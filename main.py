import sys
import requests
from zipfile import ZipFile
import pandas as pd
import glob
import os

command = input('Enter desired CPT code or type "update" to update chargemasters : ')

if command == "update":

	#this is the file which contains the chargemasters of all the California hospitals according to the CA state government
	targetURL = "https://data.chhs.ca.gov/dataset/0c315f3b-fc3c-4998-bd79-4659616c834d/resource/95e415ee-5c11-40b9-b693-ff9af7985a94/download/chargemaster-cdm-2020.zip"

	#here we put that file into a variable. We also print the name onto the command line to make sure the program is running
	downloadedFile = requests.get(targetURL, stream = True)
	print(downloadedFile.url)

	#We download the supplied zip file into this location in chunks
	with open(r"CAChargemasterSavedFile.zip", "wb") as savedZip:

		for chunk in downloadedFile.iter_content(chunk_size = 1024):

			if chunk:
				savedZip.write(chunk)

	#We extract all the files from the zip file we just downloaded and put the extracted folder in the same directory
	with ZipFile(r"CAChargemasterSavedFile.zip", "r") as targetZip:
	   # Extract all the contents of zip file in current directory
	   targetZip.extractall()
else:
	#a)we go through the extracted folder and, for every file that is in the Chargemaster CDM 2020 folder, as well as another unspecified folder, and is an xlsx:
	#b)for each chargemaster xlsx, we search for a sheet containing "1045"
	#c)we turn that sheet into a dataframe
	#d)we search that dataframe for the observation with the cdm code as a string
	#e)if the dataframe has the string version of the code we go to step print
	#f)if the dataframe does not have the string version it comes up as empty so we check if it has the integer version
	#g)the dataframe's first column is labeled after the hospital name so we take that name and place it as the value of the observation in the first column
	#h)makes sure all the charges are integers
	#i)we turn that observation into a dataframe with three specific column labels and concatenate that onto an ultimate dataframe for all the chargemasters
	#j)if the excel contains a font family with a value over 14 it causes an error which we corral over here
	#k)we sort, remove observations without charges, and print out the ultimate dataframe
	#l)convert the ultimate dataframe into an html table and create an html file with that table
	excelChargemasters = glob.glob(r"Chargemaster CDM 2020\\**\\*.xlsx",
			   recursive = True)

	allObservations = pd.DataFrame()

	#a)	   
	for excelChargemaster in excelChargemasters:	

		try:
			procedureCode = command
			excelFileChargemaster = pd.ExcelFile(excelChargemaster)
			sheetNames = excelFileChargemaster.sheet_names
			for sheetName in sheetNames:
				#b)
				if "1045" in str(sheetName):
					#c)
					df = excelFileChargemaster.parse(sheetName)
					#d)
					procedureCodeString = str(command)
					procedureCodeInt = int(command)
					#e)
					rowName = df.loc[:,"Unnamed: 1"] == procedureCodeString
					finalRow = df.loc[rowName]
					#f)
					if finalRow.empty:
						rowName = df.loc[:,"Unnamed: 1"] == procedureCodeInt
						finalRow = df.loc[rowName]
					#g)	
					goalObservation = pd.DataFrame(finalRow)
					columnList = goalObservation.columns.values.tolist()
					hospitalName = columnList[0]
					goalObservation.iloc[0,0] = hospitalName
					#h)
					goalObservation.iloc[0,2] = int(goalObservation.iloc[0,2])
					#i)
					goalObservation.columns = ["Procedure", "Code", "Charge"]
					allObservations = pd.concat([allObservations, goalObservation], axis=0, join="outer", ignore_index=True,)

		#j)				
		except:
			thisChargemaster = str(excelChargemaster)
			print("Skipping " + thisChargemaster[-70:-20])
			pass
	#k)
	allObservations = allObservations.sort_values(by="Charge", ascending=True)
	allObservations = allObservations.dropna()
	print(allObservations)
	#k)
	allObservations = allObservations.sort_values(by="Charge", ascending=True,ignore_index=True)
	allObservations = allObservations.dropna()
	print(allObservations)	
	#l)
	htmlTable = allObservations.to_html(classes='table table-striped')
	text_file = open("results.html", "w")
	text_file.write(htmlTable)
	text_file.close()
