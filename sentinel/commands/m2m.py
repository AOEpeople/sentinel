"""
login as user with user-password or as gitlab with token or via oidc flow
"""
import click

from sentinel.libs import helpers
from sentinel.oidc.proxy import Proxy


@click.command(
    context_settings=dict(
        ignore_unknown_options=True,
        allow_extra_args=True,
    )
)
@click.option("--port", help="port to listen on", default=8080)
@click.option("--client-id", help="client id")
@click.password_option("--client-secret", help="client secret")
@click.option("--issuer", help="issuer to be used to issue an access token")
@click.option("--scopes", help="scopes to ask for")
@click.option("--hosts", help="allowed hosts to pass access token to")
@click.pass_context
def m2m(ctx, port, client_id, client_secret, issuer, scopes, hosts):
    helpers.print_success(helpers.format_header("oidc client credentials proxy"))

    oidc_proxy = Proxy(
        port=port,
        client_id=client_id,
        client_secret=client_secret,
        issuer=issuer,
        hosts=hosts,
        scopes=scopes,
        cmd=ctx.args,
        context=Proxy.CONTEXT_CLIENT
    )
    return oidc_proxy.run()
