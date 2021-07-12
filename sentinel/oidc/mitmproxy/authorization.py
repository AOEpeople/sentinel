import json

from sentinel.libs import helpers
from mitmproxy import ctx

from sentinel.oidc.client import Client
from sentinel.oidc.proxy import Proxy


# pylint: disable-msg=missing-class-docstring
class Authorization:

    # pylint: disable-msg=no-self-use
    def load(self, loader):
        loader.add_option(
            name="authorization_client_id",
            typespec=str,
            default="",
            help="client_id",
        )
        loader.add_option(
            name="authorization_client_secret",
            typespec=str,
            default="",
            help="client_secre",
        )
        loader.add_option(
            name="authorization_issuer",
            typespec=str,
            default="",
            help="issuer",
        )
        loader.add_option(
            name="authorization_scopes",
            typespec=str,
            default="",
            help="scopes",
        )
        loader.add_option(
            name="authorization_hosts",
            typespec=str,
            default='[]',
            help="json list of hosts to pass authorization to",
        )
        loader.add_option(
            name="authorization_context",
            typespec=str,
            default="",
            help="authorization context, either 'user' or 'client'",
        )

    # pylint: disable-msg=no-self-use
    def request(self, flow):
        authorization_scopes = json.loads(ctx.options.authorization_scopes)
        authorization_hosts = json.loads(ctx.options.authorization_hosts)
        if flow.request.host.endswith(tuple(authorization_hosts)):
            client = Client(
                client_id=ctx.options.authorization_client_id,
                client_secret=ctx.options.authorization_client_secret,
                issuer=ctx.options.authorization_issuer,
                scopes=ctx.options.authorization_scopes
            )
            token = None
            if ctx.options.authorization_context not in [Proxy.CONTEXT_USER, Proxy.CONTEXT_CLIENT]:
                raise Exception(f"unknown context {ctx.options.authorizing_context}, use either "
                                f"'{Proxy.CONTEXT_USER}' or '{Proxy.CONTEXT_CLIENT}'")
            if ctx.options.authorization_context == Proxy.CONTEXT_CLIENT:
                token = client.authorize_client()
            if ctx.options.authorization_context == Proxy.CONTEXT_USER:
                token = client.authorize_user()
            access_token = token.access_token

            flow.request.headers["Authorization"] = f"Bearer {access_token}"
        else:
            helpers.print_warning(f"Host {flow.request.host} not in "
                                  f"authorization hosts list {tuple(authorization_hosts)}")


addons = [
    Authorization()
]
