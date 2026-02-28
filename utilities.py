########### Admin/Import/Etc ###########
# utilities to be used generally
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import ssl, threading, webbrowser
########### Deliverable ###########
HOST = "apps.qbparser-testing.test"
PORT = 8443
REDIRECT_URI = f"https://{HOST}:{PORT}/callback"
#super helpful basic/standrad error code function
def print_error(e, f="UNKNOWN"):
    """
    Helpful basic/standrad error code function. Called withing code via a try and except block.
    """
    print("Error in %s!" % (f))
    print(e)
    print(type(e))

def open_url(url: str) -> bool:
    try:
        return webbrowser.open_new_tab(url)
    except Exception:
        return False
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
            threading.Thread(target=self.server.shutdown, daemon=True).start()

        def log_message(self, format, *args):
            return
        
def create_https():
    try:
        httpd = HTTPServer((HOST, PORT), CallbackHandler)
        #Context object to negotiate highest protocol version that both client and server can use
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.check_hostname = False
        #Load private key and certificate
        ssl_context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
        #Init ssl socet and specify serer_side behaivor
        httpd.socket(ssl_context.wrap_socket(httpd.socket, server_side=True))
        httpd.serve_forever()
        httpd.server_close()
        return result
    except Exception as e:
        print_error(e, "create_https")
        return None




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


########### Main ###########

if __name__ == '__main__':
    create_https()
