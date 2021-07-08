import requests
from zipfile import ZipFile
import pandas as pd
import glob

#this is the file which contains the chargemasters of all the California hospitals according to the CA state government
targetURL = "https://data.chhs.ca.gov/dataset/0c315f3b-fc3c-4998-bd79-4659616c834d/resource/95e415ee-5c11-40b9-b693-ff9af7985a94/download/chargemaster-cdm-2020.zip"

#here we put that file into a variable. We also print the name onto the command line to make sure the program is running
downloadedFile = requests.get(targetURL, stream = True)
print(downloadedFile.url)

#We download the supplied zip file into this location in chunks
with open("C:\\Users\\Qadir\\Major Projects\\Coding\\Chargemaster\\Runtime\\CAChargemasterSavedFile.zip", "wb") as savedZip:

	for chunk in downloadedFile.iter_content(chunk_size = 1024):

		if chunk:
			savedZip.write(chunk)

#We extract all the files from the zip file we just downloaded and put the extracted folder in the same directory
with ZipFile("C:\\Users\\Qadir\\Major Projects\\Coding\\Chargemaster\\Runtime\\CAChargemasterSavedFile.zip", "r") as targetZip:
   # Extract all the contents of zip file in current directory
   targetZip.extractall()	
	
#we go through the extracted folder and, for every file that is in the Chargemaster CDM 2020 folder, as well as another unspecified folder, and is an xlsx,
#we write the name of that file in a text file and read the excel file, printing it to the command line
chargemasters = glob.glob("C:\\Users\\Qadir\\Major Projects\\Coding\\Chargemaster\\Runtime\\Chargemaster CDM 2020\\**\\*.xlsx", 
                   recursive = True)
for chargemaster in chargemasters:
	with open("listOfChargemasters.txt", "a") as text_file:
  	  text_file.write(chargemaster+"\n")
	
	thisChargemaster = pd.read_excel (chargemaster)
	print (thisChargemaster)
	
	
#base code for reading and printing excel files{
#allCAChargemasters = pd.read_excel (r"C:\\Users\\Qadir\\Major Projects\\Coding\\Chargemaster\\Runtime\\Chargemaster CDM 2020")
#print (allCAChargemasters)
#}
