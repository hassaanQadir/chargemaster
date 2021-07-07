import requests
from zipfile import ZipFile
import pandas as pd
import glob

targetURL = "https://data.chhs.ca.gov/dataset/0c315f3b-fc3c-4998-bd79-4659616c834d/resource/95e415ee-5c11-40b9-b693-ff9af7985a94/download/chargemaster-cdm-2020.zip"

downloadedFile = requests.get(targetURL, stream = True)

print(downloadedFile.url)

with open("C:\\Users\\Qadir\\Major Projects\\Coding\\Chargemaster\\Runtime\\CAChargemasterSavedFile.zip", "wb") as savedZip:

	for chunk in downloadedFile.iter_content(chunk_size = 1024):

		if chunk:
			savedZip.write(chunk)
			
with ZipFile("C:\\Users\\Qadir\\Major Projects\\Coding\\Chargemaster\\Runtime\\CAChargemasterSavedFile.zip", "r") as targetZip:
   # Extract all the contents of zip file in current directory
   targetZip.extractall()	
	
	
chargemasters = glob.glob("C:\\Users\\Qadir\\Major Projects\\Coding\\Chargemaster\\Runtime\\Chargemaster CDM 2020\\**\\*.xlsx", 
                   recursive = True)
for chargemaster in chargemasters:
	with open("listOfChargemasters.txt", "a") as text_file:
  	  text_file.write(chargemaster+"\n")
	
	theChargemaster = pd.read_excel (chargemaster)
	print (thisChargemaster)
	
	

#iterate through the extracted folder the following{
#open each child folder and append the name of the child to the grandchild file
#copy grandchild file and bring to child-level of the original folder
#delete the child folder}
#then iterate through the new child files and read and print their excel files into one huge list


#base code for reading and printing excel files{
#allCAChargemasters = pd.read_excel (r"C:\\Users\\Qadir\\Major Projects\\Coding\\Chargemaster\\Runtime\\Chargemaster CDM 2020")
#print (allCAChargemasters)
#}
