# What is the onlinechargemaster?

This website allows users in California to search for a medical procedure and receive a list of nearby hospitals, ranked by price for that procedure.


# Notes on onlinechargemaster v1.0.0

I have it running off the Python Anywhere hacker plan at hassaanQadir.pythonanywhere.com

User goes to the website, it calls app.yaml which serves index.html. User chooses a location and a procedure with a CPT code. That code is passed to main.py which uses Flask, requests, and pandas.

main.py has the functionality to download and parse a list containing all of California's chargemasters.

main.py takes the CPT code and searches for every chargemaster from a hospital within a radius of the chosen location that contains that procedure. Each observation that matches is put into one dataframe that is ranked by price low-to-high. That dataframe is served as an html table on a different page.
<br>
<img width="960" alt="home page" src="https://user-images.githubusercontent.com/86531769/196276561-27069ec0-0146-4017-849f-8e20c31d9f65.png">
<br>
<img width="960" alt="searching" src="https://user-images.githubusercontent.com/86531769/196276572-88a4f7b4-6382-457c-b371-5cec7a9527dd.png">
<br>
<img width="960" alt="results" src="https://user-images.githubusercontent.com/86531769/196276595-0c6a8da9-f1ae-4b90-b534-cef746a1a06a.png">
