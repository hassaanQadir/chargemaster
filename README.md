# What is the onlinechargemaster?

This website allows users in California to search for a medical procedure and receive a list of nearby hospitals, ranked by price for that procedure.


# Notes on onlinechargemaster v1.0.0

I have it running off the Python Anywhere hacker plan at hassaanQadir.pythonanywhere.com

User goes to the website, it calls app.yaml which serves index.html. User chooses a location and a procedure with a CPT code. That code is passed to main.py which uses Flask, requests, and pandas.

main.py has the functionality to download and parse a list containing all of California's chargemasters.

main.py takes the CPT code and searches for every chargemaster from a hospital within a radius of the chosen location that contains that procedure. Each observation that matches is put into one dataframe that is ranked by price low-to-high. That dataframe is served as an html table on a different page.
<br>
<img width="960" alt="home page" src="https://github.com/hassaanQadir/chargemaster/blob/435d26567fa4c9ce8af92c7c13b19847d9fd1cd6/onlinechargemaster%20selecting%20a%20location%20and%20procedure.png">
