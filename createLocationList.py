import requests
from zipfile import ZipFile
import pandas as pd
import glob
import os
import shutil
from flask import Flask, render_template, request, redirect, url_for, session
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy import distance, Point


app = Flask(__name__)

app.secret_key = '003137c84027b5533c98a6c763adf1ab455303c5e1'

env = ""

inRangeHospitals = "/home/hassaanQadir/.virtualenvs/inRangeHospitals"

def createLocationList():
    print("creating location list")
    #go through each subfolder in the folder of hospitals and add the name of that subfolder/hospital to a list
    with os.scandir(r"Chargemaster CDM 2020") as CAFolders:
        nameList = []
        for subfolder in CAFolders:
            if subfolder.is_dir():
                hospitalName = (subfolder.name)
                nameList.append(hospitalName)
    print("done making the basic list")
    try:
        #put that list of names through a geocoder to end up with a dataframe of each hospital with its latitude and longitude
        df = pd.DataFrame({'name': nameList})
        geolocator = Nominatim(user_agent="chargemaster")
        geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
        df['location'] = df['name'].apply(geocode)
        df['point'] = df['location'].apply(lambda loc: tuple(loc.point) if loc else None)
        dfNames = df['name']
        dfLocs = df['point']
        dfNameLocs = pd.concat([dfNames,dfLocs], axis = 1)
        print("put them into a dataframe")
        dfNameLocs.to_pickle("locationList.pkl")
        print("made a full pickle")
    except:
        #take the dataframe with hospitals and lat/long and put pickle it for use by inRange()
        dfNameLocs.to_pickle("locationList.pkl")
        print("made a short pickle")


def inRange(userLocation):
    userLocation = userLocation
    setRange = 30
    locationList = pd.read_pickle("locationList.pkl")
    nearbyHospitals = pd.DataFrame()

    for i in range(len(locationList)) :

        #evaluates distance between user and hospital
        targetDistance = distance.distance(userLocation, locationList.iloc[i, 1]).miles
        print(locationList.iloc[i,1])
        #if distance is within prescribed range, the hospital/point observation goes into another dataframe
        if targetDistance < setRange:
            nearbyHospitals = nearbyHospitals.append(locationList.iloc[i], ignore_index=True,)
        else:
            pass

    #create a list of nearby hospitals from the new dataframe
    nearbyHospitalNames = []
    for i in range(len(nearbyHospitals)):
        nearbyHospitalNames.append(nearbyHospitals.iloc[i,0])
    print(nearbyHospitalNames)

    #populate inRangeHospitals folder with only the information of nearby hospitals for tabulate() to work with
    if os.path.exists(inRangeHospitals):
        shutil.rmtree(inRangeHospitals)
    for j in range(len(nearbyHospitalNames)):
        shutil.copytree("Chargemaster CDM 2020/%s" % (nearbyHospitalNames[j]),"/home/hassaanQadir/.virtualenvs/inRangeHospitals/%s" % (j))

def tabulate(command):
	if command == "update":

		#this is the file which contains the chargemasters of all the California hospitals according to the CA state government
		targetURL = "https://data.chhs.ca.gov/dataset/0c315f3b-fc3c-4998-bd79-4659616c834d/resource/95e415ee-5c11-40b9-b693-ff9af7985a94/download/chargemaster-cdm-2020.zip"

		#here we put that file into a variable. We also print the name onto the command line to make sure the program is running
		downloadedFile = requests.get(targetURL, stream = True)
		print(downloadedFile.url)

		#We download the supplied zip file into this location in chunks
		with open(r"%sCAChargemasterSavedFile.zip" % (env), "wb") as savedZip:

			for chunk in downloadedFile.iter_content(chunk_size = 1024):

				if chunk:
					savedZip.write(chunk)

		#We extract all the files from the zip file we just downloaded and put the extracted folder in the same directory
		with ZipFile(r"%sCAChargemasterSavedFile.zip" % (env), "r") as targetZip:
		   #Extract all the contents of zip file in current directory
		   targetZip.extractall("")
	else:
		#a)we go through the extracted folder and, for every file that is in the inRangeHospitals folder, as well as another unspecified folder, and is an xlsx:
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
		excelChargemasters = glob.glob(r"%sinRangeHospitals/**/*.xlsx" % (env), recursive = True)

		allObservations = pd.DataFrame()

		#a)
		for excelChargemaster in excelChargemasters:

				try:
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
		allObservations = allObservations.sort_values(by="Charge", ascending=True,ignore_index=True)
		allObservations = allObservations.dropna()
		print(allObservations)
		#l)
		htmlTable = allObservations.to_html(classes='table table-striped')
		return (htmlTable)


@app.route("/", methods=['GET', 'POST'])
def index(form="theform"):
	#if a button is pressed, check which one it is
	if request.method == 'POST':
		#if 99282 is pressed, search for that CPT code
		if request.form.get('99282'):
			htmlTable = tabulate("99282")
			session['htmlTable'] = htmlTable
			return redirect(url_for("display"))
			pass
		#if 70450 is pressed, search for that CPT code and so on
		elif  request.form.get('70450'):
			htmlTable = tabulate("70450")
			session['htmlTable'] = htmlTable
			return redirect(url_for("display"))
			pass
		elif  request.form.get('74160'):
			htmlTable = tabulate("74160")
			session['htmlTable'] = htmlTable
			return redirect(url_for("display"))
			pass
		elif  request.form.get('72193'):
			htmlTable = tabulate("72193")
			session['htmlTable'] = htmlTable
			return redirect(url_for("display"))
			pass
		elif  request.form.get('80048'):
			htmlTable = tabulate("80048")
			session['htmlTable'] = htmlTable
			return redirect(url_for("display"))
			pass
		elif  request.form.get('update'):
			tabulate("update")
			createLocationList()
			return render_template('index.html', form=form)
			pass
		elif  request.form.get('update location'):
		    userLocation = Point(request.form.get('location'))
		    inRange(userLocation)
		    return render_template('index.html', form=form)
		    pass
		elif  request.form.get('blog'):
			return redirect(url_for("blog"))
			pass
	#if no button is pressed, show the buttons
	elif request.method == 'GET':
		return render_template('index.html', form=form)

	return render_template("index.html")

@app.route('/result')
def display():
    htmlTable = session.get('htmlTable', None)
    return htmlTable

@app.route('/blog')
def blog():
    with open("/home/hassaanQadir/.virtualenvs/blog.txt") as blog:
        return blog.read()

createLocationList()
