########### Admin/Import/Etc ###########
# utilities to be used generally
import requests
########### Deliverable ###########
#super helpful basic/standrad error code function
def print_error(e, f="UNKNOWN"):
    """
    Helpful basic/standrad error code function. Called withing code via a try and except block.
    """
    print("Error in %s!" % (f))
    print(e)
    print(type(e))

#Main Oauth2 Object
class OAuth2Config:
    def __init__(self, issuer='', auth_endpoint='', token_endpoint='', userinfo_endpoint='', revoke_endpoint='',
                 jwks_uri=''):
        self.issuer = issuer
        self.auth_endpoint = auth_endpoint
        self.token_endpoint = token_endpoint
        self.userinfo_endpoint = userinfo_endpoint
        self.revoke_endpoint = revoke_endpoint
        self.jwks_uri = jwks_uri

#call error with try/except within other functions
#def function():
#     """
#    Words.
#     """
#     try:
#   	<logic>
#     except Exception as e:
#         print_error(e, f="<function name>")
#         return None


def api_call(base_url, endpoint, auth_client, access_token=None, method='GET', headers=None, data=None ):
    base_url = 'https://sandbox-quickbooks.api.intuit.com'
    url = '{0}/v3/company/{1}/companyinfo/{1}'.format(base_url, auth_client.realm_id)
    auth_header = 'Bearer {0}'.format(auth_client.access_token)
    headers = {
        'Authorization': auth_header,
        'Accept': 'application/json'
    }
    if access_token:
        response = auth_client.get_user_info(access_token=access_token)
    else:
        response = requests.get(url, headers=headers)
    return response

########### Main ###########
def main():
    pass

if __name__ == '__main__':
    main()
