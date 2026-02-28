########### Admin/Import/Etc ###########
#Intuit Quickbooks CLI Parser by Jason Velvick and Jerome Althoff 
from authentication import *
from data_management import *
from user_management import *
from quickbooks import QuickBooks
from utilities import create_https, print_error
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
    #create_https() #Initialize and enable https frontend for oauth connections
    db = init_db()
    auth_dict = authenticate(db)
    endpoint = '/v3/company/{0}/companyinfo/{0}'.format(auth_client.realm_id)
    url = '{0}/v3/company/{1}/companyinfo/{1}'.format(base_url, auth_client.realm_id)
    auth_header = 'Bearer {0}'.format(bearer_token)
    headers = {
    'Authorization': auth_header,
    'Accept': 'application/json'
    }

    refresh_call(auth_dict['auth_client'], refresh_token=None)

if __name__ == '__main__':
    main()




































