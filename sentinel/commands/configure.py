import click

from sentinel.config.config import Config
from sentinel.config.config_repository import ConfigRepository


@click.command()
@click.option("--client-id", help="client id", prompt=True)
@click.password_option("--client-secret", help="client secret", prompt=True)
@click.option("--issuer", help="issuer to authorize against", prompt=True)
@click.option("--allowed-hosts", help="comma separated list of allowed hosts to pass access token to", prompt=True)
@click.option("--scopes", help="comma separated list of scopes to request", default="openid", prompt=True)
@click.option("--callback-port", help="port where callback is listening on", default=8099, prompt=True)
@click.option("--proxy-port", help="port where standalone proxy is listening on", default=8098, prompt=True)
@click.option("--proxy-connect-port-start", help="port range start where proxy connect is listening on", default=8000,
              prompt=True)
@click.option("--proxy-connect-port-end", help="port range end where proxy connect is listening on", default=8098,
              prompt=True)
def configure(client_id, client_secret, issuer, allowed_hosts, scopes, callback_port, proxy_port,
              proxy_connect_port_start, proxy_connect_port_end):
    scopes = [x.strip(' ') for x in scopes.split(",")]
    allowed_host = [x.strip(' ') for x in allowed_hosts.split(",")]

    configuration = Config(
        client_id=client_id,
        client_secret=client_secret,
        issuer=issuer,
        scopes=scopes,
        allowed_hosts=allowed_host,
        callback_port=callback_port,
        proxy_port=proxy_port,
        proxy_connect_port_start=proxy_connect_port_start,
        proxy_connect_port_end=proxy_connect_port_end,
    )

    repo = ConfigRepository()
    repo.set(configuration)
