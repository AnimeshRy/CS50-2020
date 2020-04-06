from sys import argv, exit
from csv import reader, DictReader

# check for arguments
if len(argv) < 3:
    print("Usage error you suck")
    exit(1)
# open dnafile
with open(argv[2]) as dnafile:
    txtfile = dnafile.readline()
    dna = txtfile
# create a dict to store k,v of csvfile
sequences = {}
# open csvfile and remove the header 'name'
with open(argv[1]) as csvfile:
    people = reader(csvfile)
    for row in people:
        csvfirstrow = row
        csvfirstrow.pop(0)
        break
# store the STR's as keys in dict and initialise them
for items in csvfirstrow:
    sequences[items] = 1
# iterate over every item in sequences and check for the STR sequence
for key in sequences:
    l = len(key)
    tempmax = 0
    temp = 0

    for i in range(len(dna)):
        # if you counted a sequence then don't count it again and start from 0
        if temp > 0:
            temp = 0
            # check for the STR sequence and and move forward
        if dna[i:i+l] == key:
            while dna[i+l:i+2*l] == dna[i:i+l]:
                temp += 1
                i += l

            if temp > tempmax:
                tempmax = temp
    sequences[key] += tempmax
# open and iterate trough the database of people
# treating each row as a dict and compare it to the sequence
with open(argv[1]) as csvfile2:
    people = DictReader(csvfile2)
    for person in people:
        match = 0
        # compares every sequences through matches and check for total STR's and then print the match before leaving the program
        for dna in sequences:
            if sequences[dna] == int(person[dna]):
                match += 1
            if match == len(sequences):
                print(person['name'])
                exit()
    print("No match")
