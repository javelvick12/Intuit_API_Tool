########### Admin/Import/Etc ###########
#Intuit Quickbooks CLI Parser by Jason Velvick and Jerome Althoff 
from authentication import *
import data_management as dm
from user_management import *
from quickbooks import QuickBooks
from utilities import print_error, init_crypto
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
    print("Attempting validation of user via Intuit")
    db = dm.init_db()
    crypto = init_crypto()
    result = authenticate(db, crypto)
    if not result: #in case of failure clean exit with response
        print("Authentication Failed")
        return
    API, auth_client, realm_id = result
    client_row = dm.lookup_db("Client", "row", column="client_id")
    if not client_row:
        dm.write_to_db("Client", {"client_id": auth_client.client_id, "client_secret": ut.encrypt_token(crypto, auth_client.client_secret), "scope": str(Scopes.ACCOUNTING), "RealmID": auth_client.realm_id})
    print("Authentication complete, Client saved")
if __name__ == '__main__':
    main()




































