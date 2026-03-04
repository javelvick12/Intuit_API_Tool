########### Admin/Import/Etc ###########
#Intuit Quickbooks CLI Parser by Jason Velvick and Jerome Althoff 
import utilities as ut
import data_management as dm
import connection_management as cm 
from authentication import *
from user_management import *
from quickbooks import QuickBooks
########### Deliverable ###########


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
        dm.write_to_db("Client", {"client_id": auth_client.client_id, "client_secret": cm.encrypt_token(crypto, auth_client.client_secret), "scope": str(Scopes.ACCOUNTING), "RealmID": auth_client.realm_id})
    print("Authentication complete, Client saved")

########### Main ###########
if __name__ == '__main__':
    main()




































