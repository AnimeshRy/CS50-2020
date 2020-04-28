
from cs50 import SQL
from csv import reader
from sys import argv

db = SQL("sqlite:///students.db")

# check for arguments
if len(argv) < 2:
    print("usage error")
    exit()

# open the csv file
with open(argv[1], newline='') as csvfile:
    characters = reader(csvfile)
    for character in characters:
        if character[0] == 'name':
            continue

        # split the name
        Name = character[0].split()
        # add none as the middle name if a middle name is not present and db will show as NULL
        if len(Name) < 3:
            db.execute("INSERT INTO students(first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)",
                       Name[0], None, Name[1], character[1], character[2])

        else:
            db.execute("INSERT INTO students(first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)",
                       Name[0], Name[1], Name[2], character[1], character[2])