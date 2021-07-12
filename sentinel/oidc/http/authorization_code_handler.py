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
            AuthorizationCodeHandler.state = auth_response["state"]
            AuthorizationCodeHandler.code = auth_response["code"]
            self.send_response(200)
            self.end_headers()
            with open(os.path.join(os.path.dirname(__file__), "../../..", "static", "oidc-ok.html")) as t:
                self.wfile.write(str.encode(t.read()))
        else:
            self.send_response(404)
            self.end_headers()
        AuthorizationCodeHandler.is_done = True

    def log_message(self, format, *args):
        return
