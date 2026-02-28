########### Admin/Import/Etc ###########
from intuitlib.client import AuthClient
from intuitlib.client import AuthClient
from hashlib import sha256
from intuitlib.exceptions import AuthClientError
from intuitlib.enums import Scopes
from quickbooks import *
from utilities import print_error, REDIRECT_URI, create_https, open_url
#from intuitlib.oath.scopes import Scopes
import data_management as dm
CLIENT_ID = "ABx3WODFu5DsxDiFiRzF6Htv6gMEhZkMYOYFqk0mIHEXzqBA7R"
CLIENT_SECRET = "RlmrGFbgmpe1tqUJNCXtt2vdqw22t1vB8kIqcFIJ"
BASE_URL = "https://sandbox-quickbooks.api.intuit.com"
ENV = "sandbox"
REALM_ID = "9341456224866626"
########### Deliverable ###########S

class Intuit_API():
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
                redirect_uri=REDIRECT_URI, 
                environment=ENV
            )
        
            return auth_client
        except AuthClientError as e:
            print_error(e, "establish_client")
    



########### Main ###########
def authenticate(db):
    API = Intuit_API(CLIENT_ID, CLIENT_SECRET, REALM_ID, BASE_URL, db)
    auth_client = API.auth_client
    if not auth_client:
        return None
    auth_url = auth_client.get_authorization_url([Scopes.ACCOUNTING]) # Fetches auth url bsed on auth_client object
    print(auth_url)
    open_url(auth_url) #Opens user browser to authenticate with Intuit
    callback = create_https()
    if not callback:
        raise RuntimeError("No callback received from HTTPS server.")
    auth_code = callback.get("code")
    realm_id = callback.get("realmId")
    if not auth_code or not realm_id:
        raise RuntimeError("Missing id or code in callback.")
    auth_client.get_bearer_token(auth_code=auth_code, realm_id=realm_id)
    



    return {
        "api": API,
        "auth_client": auth_client,
        "authorization_url": auth_url,
        "base_url": API.base_url,
        "realm_id": realm_id,
        "access_token": auth_client.access_token,
        "refresh_token": auth_client.refresh_token,
        "id_token": getattr(auth_client, "id_token", None),
    }
    

if __name__ == '__main__':
    authenticate(dm.db)