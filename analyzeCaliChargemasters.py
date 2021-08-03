import requests
from zipfile import ZipFile
import pandas as pd
import glob
import os

chromeOSPath = "unsure"
windowsPath = "C:\\Users\\Qadir\\Major Projects\\Coding\\Chargemaster\\Runtime\\"
runtimeFolder = windowsPath

#we go through the extracted folder and, for every file that is in the Chargemaster CDM 2020 folder, as well as another unspecified folder, and is an xlsx:
#a)we use some counters to create multiple destination files
#b)we write the name of that file in a text file
#c)we create an excel file object in panda, printing the names of them all for verification, 
#d)then if the excel file contains a sheet with "1045" in its title, we add that sheet to a dataframe called form1045, and print it, then rinse and repeat for each excel file
#f)trying to figure out a way that each excel file doesn't overwrite the same form1045 dataframe
#e)if the excel contains a font family with a value over 14 it causes an error which we corral over here
excelChargemasters = glob.glob(r"%sChargemaster CDM 2020\\**\\*.xlsx" % (runtimeFolder),
                   recursive = True)

#a)				   
i = 0 
j = 0		
		   
for excelChargemaster in excelChargemasters:
	j += 1
	if (j % 5 == 0):
		i += 1
	
	#b)
	#with open("listOfExcelChargemasters%d.txt" % i, "a") as text_file:
  	  #text_file.write(excelChargemaster+"\n")
	
	#c
	try:
		excelFileChargemaster = pd.ExcelFile(excelChargemaster)
		#print(excelFileChargemaster.sheet_names)	# see all sheet names
		#d)
		sheetNames = excelFileChargemaster.sheet_names
		for sheetName in sheetNames:
			if "1045" in str(sheetName):
				df = excelFileChargemaster.parse(sheetName)
				print(df.loc[df.iloc[:,1] == "74160"])
				#f)#with open("contentChargemasters%d.txt" % i, "a") as text_file:
					#text_file.write(form1045.head().to_string(index=False)+"\n")
				#print(form1045.head().to_string(index=False))
					
	#e)				
	except:
		thisChargemaster = str(excelChargemaster)
		print("It seems " +thisChargemaster + " utilizes a font family numbered over 14")
		pass
#for each chargemaster, we search for a sheet containing "AB 1045"
#for each of those chargemaster, we search each sheet for the observation with the cdm code
#then we copy that whole observation (but we only want the cdm code and the price, so maybe we don't have to copy the whole observation)
#then we put that observation, along with a column telling us what hospital it came from (the hospital name is the folder name that the chargemaster is in)
#put that observation in a dataframe
#so we get a dataframe with all the observations related to the cdm code from each hospital
#then we sort it by the charge, lowest to highest
#inshallah
