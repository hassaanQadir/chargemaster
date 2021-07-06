import requests

targetURL = "https://data.chhs.ca.gov/dataset/0c315f3b-fc3c-4998-bd79-4659616c834d/resource/95e415ee-5c11-40b9-b693-ff9af7985a94/download/chargemaster-cdm-2020.zip"

printThis = requests.get(targetURL)

print(printThis.url)

savedFile = requests.get(targetURL)

open(""C:\Users\Qadir\Major Projects\Coding\Chargemaster\theSavedFile.zip"", "w").write(savedFile.content)
