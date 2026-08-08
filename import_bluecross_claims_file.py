import csv
import pandas as pd
import pygsheets
import json
from google.oauth2 import service_account


filename = "C:\\Users\\riken\\Downloads\\MedicalClaims.csv"
modifiedfile = "C:\\Users\\riken\\Downloads\\MedicalClaims_modified.csv"


# read and store all lines into list
lines = []
with open(filename, 'r') as fp:    
    lines = fp.readlines()

# Write file
with open(modifiedfile, 'w') as fp:
    # iterate each line
    for totallines, currentline in enumerate(lines):
        if totallines not in [0,1,2,3]:
            fp.write(currentline)


# read updated file and convert to dataframe
data = pd.read_csv(modifiedfile)
df = pd.DataFrame(data)



# Remove extra columns and write to new file
df = df.drop(['Doctor Name', 'Group ID', 'Paid by Medicare', 'Paid by Other Insurance'], axis=1)

# Sorting by column "Dates of Service"
df = df.sort_values(by=['Dates of Service', 'Patient', 'Claim Number'], ascending = [True, True, True])


client = pygsheets.authorize(service_account_file='C:\\Users\\riken\\Documents\\python-384718-f700922b117e.json')

spreadsheet_url = "https://docs.google.com/spreadsheets/d/1vQ2-FZoR09iccTURVtiCx62Wl4cWAk5Utnuyu2ntfWs/edit?usp=share_link"

sheet = client.open_by_url(spreadsheet_url)
wks = sheet.worksheet_by_title('2024')


#df = pd.read_csv(modifiedfile,delimiter=',',encoding='UTF-8')
df = df.fillna('')

wks.clear("Q", "AC")

wks.set_dataframe(df, start=(1,17))





