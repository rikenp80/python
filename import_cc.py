import csv
import pandas as pd
import gspread
import pygsheets
import json
from google.oauth2 import service_account
import os
import shutil
import time


worksheet_name = "test"
root_dir = "C:\\Users\\riken\\Documents\\credit_card_statements\\"

# assign directory
account_dir = "chase"

directory = root_dir + account_dir
imported_directory = root_dir + account_dir + "\\imported"

# iterate over files that directory
for filename in os.listdir(directory):
	filepath = os.path.join(directory, filename)
	# checking if it is a file
	if os.path.isfile(filepath):
		print(filepath)

		#split import file path into parts
		filepath_split = (filepath.rsplit("\\"))
		filepath_split_len = (len(filepath_split))

		#get name of the account
		account_name = (filepath_split[filepath_split_len-2])
		print(account_name)

		#get google sheet
		client = pygsheets.authorize(service_account_file='C:\\Users\\riken\\Documents\\python-384718-f700922b117e.json')
		spreadsheet_url = "https://docs.google.com/spreadsheets/d/1pYxGFxhbWg7L_j7knR1ONBI3e85uyf__eOddQMLyCEs/edit?usp=drive_link"
		sheet = client.open_by_url(spreadsheet_url)

		#get worksheet in google sheet
		wks = sheet.worksheet_by_title(worksheet_name)


		#get last row in sheet
		gc = gspread.service_account()
		sh = gc.open("all_cc")
		temp_ws = sh.worksheet(worksheet_name)

		alldata = temp_ws.get_all_values()
		end_row = len(alldata) + 1



		#get data from text file
		data = pd.read_csv(filepath)


		#create update dataframe with only columns to import
		if account_name.startswith("chase"):
			mod_df = data.loc[:,["Transaction Date","Amount","Description","Category","Type"]]
			filename_start = filename[0:9]
			if filename_start == "Chase0270":
				account_name = "chase_sapphire_riken"
			if filename_start == "Chase5328":
				account_name = "chase_ink_anita"
			if filename_start == "Chase5762":
				account_name = "chase_freedom_anita"
			if filename_start == "Chase2629":
				account_name = "chase_sapphire_anita"
			if filename_start == "Chase1238":
				account_name = "chase_freedom_riken"																


		elif account_name == "boa":
			mod_df = data.loc[:,["Posted Date","Amount","Payee","Address","Reference Number"]]

		elif account_name.startswith("capital_one"):
			calc_amount = (data.fillna(0)["Debit"]*-1) + data.fillna(0)["Credit"]
			mod_df = data.loc[:,["Transaction Date","Description","Category"]]
			mod_df.insert(loc=1, column='Amount',value=calc_amount)
			mod_df.insert(loc=len(mod_df.columns), column='type',value="")
		
		elif account_name.startswith("wells_fargo"):
			columns = ['date','amount','1','2','description']
			df = pd.read_csv('/Users/admin/apps/courses.csv', header=None, names=columns)


			mod_df = data.loc[:,["date","amount","description"]]


		#modify data frame
		mod_df.insert(loc=0, column='account',value=account_name)
		mod_df.insert(loc=len(mod_df.columns), column='filename',value=(account_dir + "/" + filename))

		#replace nulls with empty string
		mod_df = mod_df.fillna('')

		#insert into google sheet
		wks.set_dataframe(mod_df, start=(end_row,1),copy_head=False)

		shutil.move(filepath, (imported_directory + "//" + filename))

		time.sleep(30)
