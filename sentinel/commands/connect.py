import sys
import click

from sentinel.config.config import Config
from sentinel.config.config_repository import ConfigRepository
from sentinel.libs import helpers
from sentinel.oidc.proxy import Proxy


@click.command(
    context_settings=dict(
        ignore_unknown_options=True,
        allow_extra_args=True,
    )
)
@click.pass_context
def connect(ctx):
    if len(ctx.args) == 0 or ctx.args is None:
        helpers.print_error("no cmd has been passed to execute")
        sys.exit(1)

    config = ConfigRepository.fetch(Config)
    # @todo if not a valid configuration, start an interactive process to configure client_id, client_secret, etc.

    oidc_proxy = Proxy(
        client_id=config.client_id,
        client_secret=config.client_secret,
        issuer=config.issuer,
        scopes=config.scopes,
        port=helpers.find_free_port(config.proxy_connect_port_start, config.proxy_connect_port_end),
        hosts=config.allowed_hosts,
        cmd=ctx.args,
    )
    return oidc_proxy.run()
