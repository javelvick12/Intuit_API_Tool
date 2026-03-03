########### Admin/Import/Etc ###########
# utilities to be used generally
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import http.server
from cryptography.fernet import Fernet
import os
import ssl, threading, webbrowser

########### Deliverable ###########
HOST = "apps.qbparser-testing.test"
PORT = 8443
REDIRECT_URI = f"https://{HOST}:{PORT}/callback"
#super helpful basic/standrad error code function
def print_error(e, f="UNKNOWN") -> None:
    """
    Helpful basic/standrad error code function. Called withing code via a try and except block.
    """
    print("Error in %s!" % (f))
    print(e)
    print(type(e))

def open_url(url: str) -> bool:
    """
    Helper function to open a default browser and the argument url

    Args:
        url (str) - provided url to open
    """
    try:
        return webbrowser.open_new_tab(url)
    except Exception:
        return False
    
# required elements for class instances. 
result = {"callback_url": None, "code": None, "state": None, "realmId": None}
callback_received = threading.Event()

class CallbackHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = urlparse(self.path)

            if parsed.path != "/callback":
                self.send_response(404)
                self.end_headers()
                return

            qs = parse_qs(parsed.query)
            result["code"] = qs.get("code", [None])[0]
            result["state"] = qs.get("state", [None])[0]
            result["realmId"] = qs.get("realmId", [None])[0]
            result["callback_url"] = f"{REDIRECT_URI}?{parsed.query}"

            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"OAuth received. You can close this tab.")

            callback_received.set()
 
        def log_message(self, format, *args):
            return
        
def create_https() -> dict | None:
    """
    Function creates a secure https connection

    Args:
        None

    Returns:
        (dict) if successful a secure connection
        (None) if an error for failure
    """
    #resets connection logic for the connection and values
    callback_received.clear()
    result.update({"callback_url": None, "code": None, "state": None, "realmId": None, })
    #attempt to set up connection
    try:
        httpd = http.server.HTTPServer((HOST, PORT), CallbackHandler)
        #Context object to negotiate highest protocol version that both client and server can use
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.check_hostname = False
        #Load private key and certificate
        ssl_context.load_cert_chain(certfile="keys/cert.pem", keyfile="keys/key.pem", password="Intuit_API")
        #Init ssl socet and specify server_side behaivor
        httpd.socket = ssl_context.wrap_socket(httpd.socket, server_side=True)
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        if callback_received.wait(timeout=300):
            httpd.shutdown()
            httpd.server_close()
            return result
        else:
            httpd.shutdown()
            httpd.server_close()
            return None
    except Exception as e:
        print_error(e, "create_https")
        return None

def init_crypto() -> Fernet | None:
    """
    Uses fernet from cyrptography library to create ciphersuite object, where a key can be used
    to encrypt and decrypt tokens. Key is pulled from env vars, or generated if not found (dev fallback).

    Returns:
        Fernet: ciphersuite object for encrypting and decrypting tokens. Uses FERNET_KEY from env vars, 
        or generates a new one if not found (dev fallback).
        None: if error. 
    """
    key = os.environ.get("FERNET_KEY")
    if key:
        key = key.encode()
        return Fernet(key)
    KEY_PATH = os.path.join(os.path.dirname(__file__), 'keys/fernet.key')
    try:
        if os.path.exists(KEY_PATH):
            with open(KEY_PATH, "rb") as f:
                    key = f.read().strip()
        else:
            os.makedirs(os.path.dirname(KEY_PATH), exist_ok=True)
            key = Fernet.generate_key()
            # write then restrict permissions
            with open(KEY_PATH, "wb") as f:
                f.write(key)
            os.chmod(KEY_PATH, 0o600)
            print("Generated FERNET_KEY and saved to", KEY_PATH)
        return Fernet(key)
    except Exception as e:
        print_error(e, "init_crypto")
        key = Fernet.generate_key()
        print("Using ephemeral FERNET_KEY (won't persist across runs)")
        return None

def encrypt_token(cipher: Fernet, plaintext: str) -> str:
    return cipher.encrypt(plaintext.encode()).decode()

def decrypt_token(cipher: Fernet, token_encrypted: str) -> str:
    return cipher.decrypt(token_encrypted.encode()).decode()

########### Main ###########

if __name__ == '__main__':
    create_https()
