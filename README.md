# Chargemaster v1.0.0
California Chargemaster: A Hospital Chargemaster Aggregator

Google account: chargemasteronline@gmail.com
I have a version of this saved on Google's Cloud shell but I couldn't get it to work.

Python Anywhere: hassaanQadir
So I have it running off the Python Anywhere hacker plan at hassaanQadir.pythonanywhere.com

User goes to the website, it calls app.yaml which serves index.html. User chooses a location and a procedure with a CPT code. That code is passed to main.py which uses Flask, requests, and pandas.

main.py has the functionality to download and parse a list containing all of California's chargemasters.

main.py takes the CPT code and searches for every chargemaster from a hospital within a radius of the chosen location that contains that procedure. Each observation that matches is put into one dataframe that is ranked by price low-to-high. That dataframe is served as an html table on a different page.
