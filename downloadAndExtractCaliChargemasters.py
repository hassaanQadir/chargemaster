import requests
from zipfile import ZipFile
import pandas as pd
import glob
import os

#this is the file which contains the chargemasters of all the California hospitals according to the CA state government
targetURL = "https://data.chhs.ca.gov/dataset/0c315f3b-fc3c-4998-bd79-4659616c834d/resource/95e415ee-5c11-40b9-b693-ff9af7985a94/download/chargemaster-cdm-2020.zip"

#here we put that file into a variable. We also print the name onto the command line to make sure the program is running
downloadedFile = requests.get(targetURL, stream = True)
print(downloadedFile.url)

chromeOSPath = "unsure"
windowsPath = "C:\\Users\\Qadir\\Major Projects\\Coding\\Chargemaster\\Runtime\\"
runtimeFolder = windowsPath

#We download the supplied zip file into this location in chunks
with open(r"%sCAChargemasterSavedFile.zip" % (runtimeFolder), "wb") as savedZip:

	for chunk in downloadedFile.iter_content(chunk_size = 1024):

		if chunk:
			savedZip.write(chunk)

#We extract all the files from the zip file we just downloaded and put the extracted folder in the same directory
with ZipFile(r"%sCAChargemasterSavedFile.zip" % (runtimeFolder), "r") as targetZip:
   # Extract all the contents of zip file in current directory
   targetZip.extractall()
