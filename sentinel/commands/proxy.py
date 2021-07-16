"""
login as user with user-password or as gitlab with token or via oidc flow
"""
import click

from sentinel.config.config import Config
from sentinel.config.config_repository import ConfigRepository
from sentinel.context import Context
from sentinel.libs import helpers
from sentinel.oidc.proxy import Proxy


@click.command()
def proxy():
    Context.verbose = True

    config = ConfigRepository.fetch(Config)

    helpers.print_success(helpers.format_header("oidc proxy"))
    helpers.print_info(f"proxy started on port {config.proxy_port} intercepting hosts {config.allowed_hosts}:")
    helpers.print_info(f"export http_proxy=http://localhost:{config.proxy_port}")
    helpers.print_info(f"export https_proxy=http://localhost:{config.proxy_port}")

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
