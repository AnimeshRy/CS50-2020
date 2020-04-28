from cs50 import SQL
from sys import argv

# check for arguments
if len(argv) != 2:
    print("usage error")
    exit()
# open the db and store it in db variable
db = SQL("sqlite:///students.db")

housename = argv[1]

# store the query inside roster
roster = db.execute("SELECT * FROM students WHERE house = (?) ORDER BY last", housename)

# iterate over the roster to get the desired result
for row in roster:
    if row['middle'] != None:
        print("{} {} {}, born {}".format(row['first'], row['middle'], row['last'], row['birth']))
    else:
        print("{} {}, born {}".format(row['first'], row['last'], row['birth']))