#Intuit Quickbooks CLI Parser by Jason Velvick and Jerome Althoff
from intuitlib.client import AuthClient
from intuitlib.enums import Scopes














































if __name__ == "__main__":
    auth_client = AuthClient( client_id, client_secret, redirect_uri, environment )
    url = auth_client.get_authorization_url([Scopes.ACCOUNTING])