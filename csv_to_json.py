
import csv
import json

csvfile = open(r'C:\Users\rpatel3\Documents\paypal_cc\2021_03.csv', 'r')
jsonfile = open(r'C:\Users\rpatel3\Documents\paypal_cc\2021_03.json', 'w')

fieldnames = ("Transaction Date","Posting Date","Reference Number","Amount","Description")
reader = csv.DictReader(csvfile, fieldnames)

for row in reader:
        json.dump(row, jsonfile)
        jsonfile.write('\n')