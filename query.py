import sys
import requests
from zipfile import ZipFile
import pandas as pd
import glob
import os

chromeOSPath = "unsure"
windowsPath = "C:\\Users\\Qadir\\Major Projects\\Coding\\Chargemaster\\Runtime\\"
runtimeFolder = windowsPath

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
excelChargemasters = glob.glob(r"%sChargemaster CDM 2020\\**\\*.xlsx" % (runtimeFolder),
                   recursive = True)

allObservations = pd.DataFrame()
				   
#a)	   
for excelChargemaster in excelChargemasters:	
	
	try:
		procedureCode = sys.argv[1]
		excelFileChargemaster = pd.ExcelFile(excelChargemaster)
		sheetNames = excelFileChargemaster.sheet_names
		for sheetName in sheetNames:
			#b)
			if "1045" in str(sheetName):
				#c)
				df = excelFileChargemaster.parse(sheetName)
				#d)
				procedureCodeString = str(sys.argv[1])
				procedureCodeInt = int(sys.argv[1])
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
		print("It seems " +thisChargemaster + " utilizes a font family numbered over 14")
		pass
#k)
allObservations = allObservations.sort_values(by="Charge", ascending=True)
allObservations = allObservations.dropna()
print(allObservations)

#so we get a dataframe with all the observations related to the cdm code from each hospital
#then we sort it by the charge, lowest to highest
#inshallah
