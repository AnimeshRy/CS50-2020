import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    portfolio = db.execute("SELECT symbol, SUM(shares) as number_of_shares, price FROM transactions WHERE user_id = :user_id GROUP BY symbol", user_id=session["user_id"])

    rows = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])

    available_cash = rows[0]["cash"]

    return render_template("index.html", portfolio=portfolio, available_cash=available_cash)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buying some stocks"""

    if request.method == "POST":

        stock = lookup(request.form.get("symbol"))

        if stock == None:
            return apology("invalid ticker symbol")

        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("Enter a integer here - ")

        if shares < 0:
            return apology("enter a positive amount")

        rows = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id = session["user_id"])

        available_cash = rows[0]["cash"]

        price = stock["price"]

        total_price = shares * price

        if available_cash < total_price:
            return apology("insufficient funds")

        db.execute("UPDATE users SET cash = cash - :total_price WHERE id = :user_id", total_price=total_price, user_id=session["user_id"])
        db.execute("INSERT INTO 'transactions' (user_id, symbol, shares, price) VALUES (:user_id, :symbol, :shares, :price)", user_id=session["user_id"], symbol=request.form.get("symbol"), shares=shares, price=price)

        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute("SELECT symbol, shares, price, timestamp FROM transactions WHERE user_id = :user_id", user_id=session["user_id"])

    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":

        stock = lookup(request.form.get("symbol"))

        if not stock:
            return apology("Can't find your stock")

        return render_template ("quote.html",stock=stock)

    else:
        return render_template ("quote.html",stock="")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    #checking for correct input
    if request.method == "POST":

        if not request.form.get("username"):
            return apology("must provide username",403)

        elif not request.form.get("password"):
            return apology("wrong password",403)

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("wrong confirmation",403)

         # Query database for username if already exists
        elif db.execute("SELECT * FROM users WHERE username = :username",
            username=request.form.get("username")):
            return apology("Username already taken", 403)

        # Insert user and hash of the password into the table
        db.execute("INSERT INTO users(username, hash) VALUES (:username, :hash)",
            username=request.form.get("username"), hash=generate_password_hash(request.form.get("password")))

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
            username=request.form.get("username"))

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":

        stock = lookup(request.form.get("symbol"))

        if stock == None:
            return apology("invalid ticker symbol")

        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("must be a number")

        if shares < 0:
            return apology("input positive number")

        available_shares = db.execute("SELECT SUM(shares) as total_shares FROM transactions WHERE user_id = :user_id and symbol = :symbol GROUP BY symbol",
                                        user_id=session["user_id"], symbol=request.form.get("symbol"))

        if available_shares[0]["total_shares"] < 1 or shares > available_shares[0]["total_shares"]:
            return apology("not enough shares")

        price = stock["price"]

        total_price = shares * price

        db.execute("UPDATE users SET cash = cash + :total_price WHERE id = :user_id", user_id=session["user_id"], total_price=total_price)
        db.execute("INSERT INTO 'transactions' (user_id, symbol, shares, price) VALUES(:user_id, :symbol, :shares, :price)", user_id=session["user_id"], symbol=request.form.get("symbol"), shares=-shares, price=price)

        return redirect("/")

    else:
        available_stocks = db.execute("SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = :user_id GROUP BY symbol", user_id=session["user_id"])
        return render_template("sell.html", available_stocks=available_stocks)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
