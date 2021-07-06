import requests

targetURL = "https://data.chhs.ca.gov/dataset/0c315f3b-fc3c-4998-bd79-4659616c834d/resource/95e415ee-5c11-40b9-b693-ff9af7985a94/download/chargemaster-cdm-2020.zip"

savedFile = requests.get(targetURL, stream = True)

print(savedFile.url)

with open("C:\Users\Qadir\Major Projects\Coding\Chargemaster\theSavedFile.zip", "w") as savedZip:

	for chunk in savedFile.iter_content(chunk_size = 1024):

		if chunk:

			savedZip.write(chunk)
