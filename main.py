import requests
from zipfile import ZipFile
import pandas as pd
import glob
import os
from flask import Flask, render_template, request, redirect, url_for, session
from geopy.geocoders import Nominatim
import time


app = Flask(__name__)

app.secret_key = '003137c84027b5533c98a6c763adf1ab455303c5e1'

env = ""

def inRange():
    with os.scandir(r"Chargemaster CDM 2020") as CAFolders:
        for subfolder in CAFolders:
            if subfolder.is_dir():
                hospitalName = str(subfolder.name)
                print(hospitalName)
                #Google Place API

                #SmartyStreets


                #Nominatim
                try:
                    loc = Nominatim(user_agent="GetLoc")
                    getLoc = loc.geocode(hospitalName)
                    print(getLoc.address)
                    time.sleep(1)
                    print("Longitude = ", getLoc.longitude)
                    print("Latitude = ", getLoc.latitude, "\n")
                except(AttributeError):
                    print("Couldn't find address")
                    pass
inRange()

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
		#l)convert the ultimate dataframe into an html table and create an html file with that table
		excelChargemasters = glob.glob(r"%sChargemaster CDM 2020/**/*.xlsx" % (env), recursive = True)

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
		if request.form.get('action1') == 'Emergency Room Visit Level 2 (low to moderate severity) 99282':
			htmlTable = tabulate("99282")
			session['htmlTable'] = htmlTable
			return redirect(url_for("display"))
			pass
		#if 70450 is pressed, search for that CPT code and so on
		elif  request.form.get('action2') == 'CT Scan Head or Brain, without contrast 70450':
			htmlTable = tabulate("70450")
			session['htmlTable'] = htmlTable
			return redirect(url_for("display"))
			pass
		elif  request.form.get('action3') == 'CT Scan, Abodemen, with contrast 74160':
			htmlTable = tabulate("74160")
			session['htmlTable'] = htmlTable
			return redirect(url_for("display"))
			pass
		elif  request.form.get('action4') == 'CT Scan, Pelvis, with contrast 72193':
			htmlTable = tabulate("72193")
			session['htmlTable'] = htmlTable
			return redirect(url_for("display"))
			pass
		elif  request.form.get('action5') == 'Basic Metabolic Panel 80048':
			htmlTable = tabulate("80048")
			session['htmlTable'] = htmlTable
			return redirect(url_for("display"))
			pass
		elif  request.form.get('action6') == 'Update Chargemasters':
			htmlTable = tabulate("update")
			return htmlTable
			pass
	#if no button is pressed, show the buttons
	elif request.method == 'GET':
		return render_template('index.html', form=form)

	return render_template("index.html")

@app.route('/result')
def display():
    htmlTable = session.get('htmlTable', None)
    return htmlTable
