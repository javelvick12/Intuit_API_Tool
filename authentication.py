########### Admin/Import/Etc ###########
from intuitlib.client import AuthClient
from intuitlib.client import AuthClient
from intuitlib.exceptions import AuthClientError
from intuitlib.enums import Scopes
from quickbooks import *
from cryptography.fernet import Fernet 
import connection_management as cm  
#from intuitlib.oath.scopes import Scopes
import data_management as dm
BASE_URL = "https://sandbox-quickbooks.api.intuit.com"
ENV = "sandbox"

########### Deliverable ###########S
class Intuit_API():
    """
    Creates a class of API for Intuit connection. 
    """
    def __init__(self, client_id, client_secret, realm_id, base_url, db=None):
        self.client_id = client_id # Our unique client ID for our Intuit application
        self.realm_id = realm_id #Our QuickBooks Sandbox unique identifier.
        self.base_url = base_url
        self.client_secret = client_secret
        self.auth_client = self.establish_client(db)
    def establish_client(self, db: dm.sa.Engine | None) -> AuthClient | None:
        try:
            auth_client = AuthClient(
                client_id=self.client_id,
                client_secret=self.client_secret,
                redirect_uri=cm.REDIRECT_URI, 
                environment=ENV
            )
            return auth_client
        except AuthClientError as e:
            cm.print_error(e, "establish_client")
            return None

########### Main ###########
def authenticate(db: dm.sa.engine, crypto: Fernet):
    """
    Autehtnication logic. 
        args:
            db (SQLAlchamy) - queries user creds
            crypto (Fernet) - decrypts pws 
        returns:
            tuple: API, auth_client, realm_id
    """
    try:
        client = dm.lookup_db("Client", "row")
        if not client:
            while True:
                print("***No client information found. Please enter client information***\n")
                client_id = str(input("Enter Intuit Client ID: ")).strip()
                client_secret = str(input("Enter Intuit Client Secret: ")).strip()
                realm_id = str(input("Enter Company/Realm ID: ")).strip()
                if client_id and client_secret and realm_id:
                    break
                else:
                    missing = [name for name, val in [("Client ID", client_id), ("Client Secret",  client_secret), ("Realm ID", realm_id)] if not val]
                    print(f"Missing parameters {', '.join(missing)}. Try again.") #DEBUG made feedback dynamic 
        else:
            client_id = client[0]["client_id"]
            client_secret_cipher = client[0]["client_secret"]
            client_secret = cm.decrypt_token(crypto, client_secret_cipher)
            realm_id = client[0]["RealmID"]
        API = Intuit_API(client_id, client_secret, realm_id, BASE_URL, db)
        auth_client = API.auth_client
        if not auth_client:
            return None
        auth_url = auth_client.get_authorization_url([Scopes.ACCOUNTING]) # Fetches auth url bsed on auth_client object
        print("navigating to auth url:", auth_url)
        cm.open_url(auth_url) #Opens user browser to authenticate with Intuit
        callback = cm.create_https()
        if not callback:
            raise RuntimeError("No callback received from HTTPS server.")
        auth_code = callback.get("code")
        realm_id = callback.get("realmId")
        if not auth_code or not realm_id:
            raise RuntimeError("Missing id or code in callback.")
        auth_client.get_bearer_token(auth_code=auth_code, realm_id=realm_id)
        encrypted_access_token = cm.encrypt_token(crypto, auth_client.access_token)
        encrypted_refresh_token = cm.encrypt_token(crypto, auth_client.refresh_token)
        access_to_write = {"token_hash": encrypted_access_token, "token_type": "access", "client_id": auth_client.client_id}
        dm.write_to_db("Token", access_to_write)
        refresh_to_write = {"token_hash": encrypted_refresh_token, "token_type": "refresh", "client_id": auth_client.client_id}
        dm.write_to_db("Token", refresh_to_write)
        return API, auth_client, realm_id
    except Exception as e:
        cm.print_error(e, "authenticate")
        return None

if __name__ == '__main__':
    authenticate(dm.db)