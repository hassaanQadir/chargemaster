import requests
from zipfile import ZipFile

targetURL = "https://data.chhs.ca.gov/dataset/0c315f3b-fc3c-4998-bd79-4659616c834d/resource/95e415ee-5c11-40b9-b693-ff9af7985a94/download/chargemaster-cdm-2020.zip"

downloadedFile = requests.get(targetURL, stream = True)

print(downloadedFile.url)

with open("C:\\Users\\Qadir\\Major Projects\\Coding\\Chargemaster\\CAChargemasterSavedFile.zip", "wb") as savedZip:

	for chunk in savedZip.iter_content(chunk_size = 1024):

		if chunk:
			savedZip.write(chunk)
			
with ZipFile('savedZip', 'r') as targetZip:
   # Extract all the contents of zip file in current directory
   targetZip.extractall()			
