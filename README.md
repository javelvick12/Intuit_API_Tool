# Intuit_API_Tool
Final project for COMP 4705 by Jason Velvick and Jerome Althoff. This terminal based tool is a python program that interacts with the Intuit developer API to fetch data of interest from QuickBooks Online. 
Python Libraries Used:
python-quickbooks 0.9.12
intuit-oauth 1.2.6

Purpose:
    ##############words##############

Functionality:
    Project is run from root via CLI "python3 main.py <arguments? api key, destination, ....?>"

Required Dependencies:
    Intuit libarary oauth, quick books...? 

Errors:
    ##############words##############

Licenses Involved:
    Python-Quickbooks
        License: MIT License (MIT)
        Author: Edward Emanuel Jr.
    Intuit-Oauth
        License: Apache 2.0
        Author: Intuit Inc
##############Anything else?##############
Steps to run:

1. Must map apps.qbparser-testing.test to 127.0.0.1 in your OS DNS config

2. Use requirements.txt to install needed pip packages for the app with pip install -r requirements.txt  

3. If there are no clients in the Clients table, you will be prompted to enter client id client secret and realm id

4. May run into permission issues with some of the crypto files and operations, let me know if you do.




