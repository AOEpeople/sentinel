from typing import List


class Config:
    client_id: str
    client_secret: str
    issuer: str
    scopes: List[str]
    allowed_hosts: List[str]
    callback_port: int
    proxy_port: int
    proxy_connect_port_start: int
    proxy_connect_port_end: int

    def __init__(
            self,
            client_id: str,
            client_secret: str,
            issuer: str,
            scopes: List[str],
            allowed_hosts: List[str],
            callback_port: int,
            proxy_port: int,
            proxy_connect_port_start: int,
            proxy_connect_port_end: int,
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.issuer = issuer
        self.scopes = scopes
        self.allowed_hosts = allowed_hosts
        self.callback_port = callback_port
        self.proxy_port = proxy_port
        self.proxy_connect_port_start = proxy_connect_port_start
        self.proxy_connect_port_end = proxy_connect_port_end
