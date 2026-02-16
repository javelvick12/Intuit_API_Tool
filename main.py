########### Admin/Import/Etc ###########
#Intuit Quickbooks CLI Parser by Jason Velvick and Jerome Althoff 
from authentication import *
from data_management import *
from user_management import *
from quickbooks import QuickBooks
from utilities import api_call, print_error
import requests
########### Deliverable ###########

def refresh_call(auth_client, refresh_token):
    try:
        new_token = auth_client.refresh(refresh_token)
        return new_token
    except ValueError as e:
        print_error(e, f="Refresh Call")
        return None



########### Main ###########
def main():
    base_url = 'https://sandbox-quickbooks.api.intuit.com'
    endpoint = '/v3/company/{0}/companyinfo/{0}'.format(auth_client.realm_id)
    url = '{0}/v3/company/{1}/companyinfo/{1}'.format(base_url, auth_client.realm_id)
    auth_header = 'Bearer {0}'.format(auth_client.access_token)
    headers = {
    'Authorization': auth_header,
    'Accept': 'application/json'
    }

    try:
        response = api_call(base_url, endpoint, auth_client,  method='GET', headers=None, data=None)
    except requests.exceptions.RequestException as e:
        print_error(e, f="API Call")
        return None
    
    refresh_call(auth_client, refresh_token=None)

if __name__ == '__main__':
    main()




































