import sys
import csv
import re

if len(sys.argv) != 3:
    sys.exit("Usage: python dna.py data.csv sequence.txt")
if not ".csv" in sys.argv[1]:
    sys.exit("Usage: python dna.py data.csv sequence.txt")
if not ".txt" in sys.argv[2]:
    sys.exit("Usage: python dna.py data.csv sequence.txt")

matches = {}
# open csv file
with open(sys.argv[1], "r") as csv_file:
    reader = csv.DictReader(csv_file)
    header = reader.fieldnames[1:]  # header = dict of field names excluding first one (name)

    # open txt file
    with open(sys.argv[2], "r") as txt_file:
        seq = txt_file.read()

        # iterate through sequences in the header
        for head in header:
            # = find all matches in .txt file and group those, that occure sequentially in a test list
            # and if test list, returned by findall is empty, then no matches exist in the .txt file and we should exit
            test = re.findall(f"(?:{head})+", seq)
            if len(test) < 1:
                sys.exit("No match")
            # find longest group in a test list and calculate how many sequences in that group,
            # by deviding length of group by length of sequence
            matches[head] = int(len(max(test)) / len(head))

    # iterate through dictionaries in a list, that containes set of person data
    for index in reader:
        # for each person set count of matches sequences to 0
        M = 0
        
        # for each key in persons dictionary skip name key and convert rest of values to integers
        for key in index:
            if key == "name":
                continue
            else:
                index[key] = int(index[key])

        # for each key(sequence) in .txt file, if number of sequences == number of sequences of person, add count matches
        for key in matches:
            if matches[key] == index[key]:
                M += 1

        # if number of matches between .txt file and person == number of sequences that we searched,
        # print name of that person and exit
        if M == len(header):
            sys.exit(index["name"])

# if nothing was found, exit
sys.exit("No match")
