import os
import webbrowser
from typing import List

from sentinel.config.config import Config
from sentinel.config.config_repository import ConfigRepository
from sentinel.libs import helpers
from sentinel.oidc.exceptions import RefreshTokenException
from sentinel.oidc.http.authorization_code_handler import AuthorizationCodeHandler
from sentinel.oidc.token import Token

import http.server

import oic
from oic.oauth2 import CCAccessTokenRequest
from oic.oic import Client as OicClient
from oic.utils.authn.client import CLIENT_AUTHN_METHOD
from oic.oic.message import RegistrationResponse, AccessTokenResponse
from oic import rndstr
from oic.oauth2 import REQUEST2ENDPOINT

from sentinel.oidc.token_repository import TokenRepository


class Client:
    client_id: str = None
    client_secret: str = None
    issuer: str = None
    scopes: List[str] = None

    use_cache: bool = None

    oic_client: "OicClient" = None
    token_repository: "TokenRepository" = None
    client_credentials_secret: str = None

    def __init__(
            self,
            client_id: str,
            client_secret: str,
            issuer: str,
            scopes: List[str],
            use_cache: bool = True
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.issuer = issuer
        self.scopes = scopes
        self.use_cache = use_cache
        self.oic_client = self.__create_oic_client()
        self.token_repository = TokenRepository()

    def authorize_client(self):
        return self.__login_using_client_credentials()

    def authorize_user(self):
        if self.token_repository.exists() and self.use_cache is not False:
            token = self.token_repository.get()
            if token.is_expired() is False:
                return token
            try:
                return self.__refresh_token(token)
            except RefreshTokenException:
                pass
        return self.__login_using_authorization_code()

    def __login_using_client_credentials(self) -> Token:
        session = {"state": rndstr()}

        args = {
            "client_id": self.oic_client.client_id,
            "client_secret": self.oic_client.client_secret,
            "grant_type": "client_credentials",
            "scope": f"https://narf.tech/{os.getenv('CLUSTER', 'ops-dev')}",
            "state": session["state"],
        }

        # @todo find out how to replace this with `construct_AccessTokenRequest`
        url, body, ht_args, _ = self.oic_client.request_info(CCAccessTokenRequest, request_args=args)

        token_response = self.oic_client.request_and_return(response=AccessTokenResponse, url=url, method="POST",
                                                            body=body,
                                                            http_args=ht_args)

        return Token(access_token=token_response["access_token"])

    def __login_using_authorization_code(self) -> Token:
        session = {"state": rndstr(), "nonce": rndstr()}

        config = ConfigRepository.fetch(Config)

        args = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "response_type": "code",
            "scope": self.scopes,
            "nonce": session["nonce"],
            "redirect_uri": [f"http://localhost:{config.callback_port}/oidc/callback"],
            "state": session["state"]
        }

        auth_req = self.oic_client.construct_AuthorizationRequest(request_args=args)
        login_url = auth_req.request(self.oic_client.authorization_endpoint)

        http_handler = AuthorizationCodeHandler
        http_handler.client = self.oic_client
        http_handler.is_done = False
        http_handler.state = None
        http_handler.code = None

        with http.server.HTTPServer(("localhost", config.callback_port), http_handler) as httpd:
            helpers.print_info(
                f"if not opening automatically, please open the following url in your browser: {login_url}")
            webbrowser.open(login_url)
            while not http_handler.is_done:
                httpd.handle_request()

        if http_handler.state is None or http_handler.code is None:
            raise Exception(f"could not get state ({http_handler.state}) or code ({http_handler.code})")

        if http_handler.state != session["state"]:
            raise Exception(f"Session state is compromised! Initial state: {session['state']} "
                            f"!= received state: {http_handler.state}")

        token_response = self.oic_client.do_access_token_request(state=http_handler.state,
                                                                 scope=",".join(self.scopes),
                                                                 request_args={"code": http_handler.code},
                                                                 authn_method="client_secret_basic",
                                                                 skew=10)

        if "id_token" not in token_response:
            raise Exception(f"could not find id_token in token response: {token_response}")

        if token_response["id_token"]["nonce"] != session["nonce"]:
            raise Exception(f"requested nonce {session['nonce']} does"
                            f"not match nonce in token: {token_response['id_token']['nonce']}")

        token_response["id_token_raw"] = self.oic_client._get_id_token(state=http_handler.state)

        token = Token(
            access_token=token_response["access_token"],
            refresh_token=token_response["refresh_token"],
            id_token=token_response["id_token_raw"],
            expires_in=token_response["expires_in"]
        )
        token.renew_expires_at_from_now()

        self.__store_token(token)

        return token

    def __refresh_token(self, token: "Token") -> Token:
        session = {"state": rndstr(), "nonce": rndstr()}
        refresh_args = {
            "client_id": self.oic_client.client_id,
            "state": session["state"],
            "grant_type": "refresh_token",
            "refresh_token": token.refresh_token
        }
        self.oic_client.request2endpoint = REQUEST2ENDPOINT

        token_oic = oic.oauth2.Token()
        token_oic.refresh_token = token.refresh_token

        response = self.oic_client.do_access_token_refresh(
            request_args=refresh_args,
            state=session["state"],
            token=token_oic,
            skew=10  # @todo https://github.com/OpenIDC/pyoidc/issues/785
        )
        if "access_token" not in response or "expires_in" not in response:
            raise RefreshTokenException(response)

        token.access_token = response["access_token"]
        token.expires_in = response["expires_in"]
        token.renew_expires_at_from_now()

        self.__store_token(token)

        return token

    def __create_oic_client(self) -> "OicClient":
        client = OicClient(client_authn_method=CLIENT_AUTHN_METHOD)

        # START - never remove the following line!!!!!!
        client.request2endpoint = REQUEST2ENDPOINT
        # END   - never remove the following line!!!!!!

        client.provider_config(self.issuer)
        info = {"client_id": self.client_id,
                "client_secret": self.client_secret}
        client_reg = RegistrationResponse(**info)

        client.store_registration_info(client_reg)
        return client

    def __store_token(self, token: "Token"):
        if self.use_cache is not False:
            self.token_repository.set(token)
