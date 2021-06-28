import requests

r = requests.get('https://bayareahospital.org/patient-resources/')

print(r.url)
