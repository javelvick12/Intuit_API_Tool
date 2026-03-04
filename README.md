# Intuit_API_Tool
Final project for COMP 4705 by Jason Velvick and Jerome Althoff. This terminal based tool is a python program that interacts with the Intuit developer API to fetch data of interest from QuickBooks Online. 

Python Libraries Used:
    python-quickbooks 0.9.12
    intuit-oauth 1.2.6
    intuit-oauth
    .Net Framework 4.6.1
    Microsoft.Net.Compilers 2.10.0

Purpose:
    ##############words##############

Functionality:
    Project is run from root via CLI "python3 main.py <arguments? api key, destination, ....?>" [DEBUG]

Required Dependencies:
    Intuit libarary oauth, quick books...? <update as needed> [DEBUG]

Design:
    Root: logic in associated files, sql db, readme, process documentation (class deliverable)
    Sub-dirs: Keys (store keys); dashboard_reports (store generated reports); data_files (locally stored Intuit products)
    !!!! REMOVE helloworlds DIR !!!! [DEBUG]

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

    2. If there are no clients in the Clients table, you will be prompted to enter client id client secret and realm id

    3. Create and use a Virtual Environemnt
        Create:
            $ python3 -m venv <name of virtual environement, example IntuitVenv>
            $ python3 -m venv IntuitVenv 
        Use (from project root):
            ┌──(user㉿machine)-[project path]
            └─$ source IntuitVenv/bin/activate  

    4. Get required packages
        Run:
            $ pip install -r requirements.txt 
        Update as required: 
            $ pip update -r requirements.txt

    5. May run into permission issues with some of the crypto files and operations, let me know if you do.

    6. Stop virtual environment from within the virtual environment:
        ┌──(IntuitVenv)─(user㉿machine)-[project path]
        └─$ deactivate

