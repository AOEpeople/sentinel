"""
login as user with user-password or as gitlab with token or via oidc flow
"""
import click

from sentinel.config.config import Config
from sentinel.config.config_repository import ConfigRepository
from sentinel.libs import helpers
from sentinel.oidc.proxy import Proxy


@click.command()
@click.pass_context
def proxy():
    helpers.print_success(helpers.format_header("oidc proxy"))
    helpers.print_info("export http_proxy=http://localhost:8098")
    helpers.print_info("export https_proxy=http://localhost:8098")

    config = ConfigRepository.fetch(Config)
    # @todo if not a valid configuration, start an interactive process to configure client_id, client_secret, etc.

    oidc_proxy = Proxy(
        client_id=config.client_id,
        client_secret=config.client_secret,
        issuer=config.issuer,
        scopes=config.scopes,
        port=config.proxy_port,
        hosts=config.allowed_hosts,
    )
    return oidc_proxy.run()
