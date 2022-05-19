import http.server
import os
import urllib.parse
from oic.oic import Client, AuthorizationResponse


class AuthorizationCodeHandler(http.server.BaseHTTPRequestHandler):
    is_done: bool = False
    state: str = None
    code: str = None
    client: Client = None

    # pylint: disable-msg=invalid-name
    def do_GET(self):
        if "/oidc/callback" in self.path:
            query = urllib.parse.urlparse(self.path).query
            auth_response = self.client.parse_response(AuthorizationResponse,
                                                       info=query,
                                                       sformat="urlencoded")
            if "error_description" in auth_response:
                self.send_error(500, auth_response["error_description"])
            else:
                if "state" in auth_response or "code" in auth_response:
                    AuthorizationCodeHandler.state = auth_response["state"]
                    AuthorizationCodeHandler.code = auth_response["code"]
                    with open(os.path.join(os.path.dirname(__file__), "../../..", "static", "oidc-ok.html")) as t:
                        self.send_response(200)
                        self.send_header('Connection', 'close')
                        self.end_headers()
                        self.wfile.write(str.encode(t.read()))
                else:
                    self.send_error(500, f"could not get state or code from callback query: {query}")

        else:
            self.send_error(404)

        AuthorizationCodeHandler.is_done = True

    def log_message(self, format, *args):
        return
