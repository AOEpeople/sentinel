import json
import os
from typing import List

from mitmproxy.tools.main import mitmdump


class Proxy:
    CONTEXT_USER: str = "user"
    CONTEXT_CLIENT: str = "client"

    def __init__(self, port, client_id: str, client_secret: str, issuer: str, scopes: List[str],
                 hosts: List[str] = None, cmd: List[str] = None, context=CONTEXT_USER):
        self.port = port
        self.client_id = client_id
        self.client_secret = client_secret
        self.issuer = issuer
        self.scopes = scopes
        self.hosts = hosts
        self.cmd = cmd
        self.context = context

    def run(self):
        args = []
        args += self.__get_executor_args()
        args += self.__get_authorization_args()
        args += self.__get_allowed_hosts_args()
        args += ["--set", f"listen_port={self.port}"]
        args += ["--quiet"]
        return mitmdump(args)

    def __get_executor_args(self) -> List[str]:

        if self.cmd is None:
            return []

        return ['-s', f"{self.__get_file_path()}/mitmproxy/executor.py", "--set",
                f"executor_cmd={json.dumps(self.cmd)}"]

    def __get_authorization_args(self) -> List[str]:
        args = [
            '-s', f"{self.__get_file_path()}/mitmproxy/authorization.py",
        ]
        args += ["--set", f"authorization_context={self.context}"]
        args += ["--set", f"authorization_client_id={self.client_id}"]
        args += ["--set", f"authorization_client_secret={self.client_secret}"]
        args += ["--set", f"authorization_scopes={json.dumps(self.scopes)}"]
        args += ["--set", f"authorization_issuer={self.issuer}"]
        if self.hosts is not None:
            args += ["--set", f"authorization_hosts={json.dumps(self.hosts)}"]

        return args

    def __get_allowed_hosts_args(self) -> List[str]:
        if self.hosts is None:
            return []
        allow_hosts = []
        for host in self.hosts:
            allow_hosts += ['--allow-hosts', f'^.*{host}:80$']
            allow_hosts += ['--allow-hosts', f'^.*{host}:443$']
        return allow_hosts

    @staticmethod
    def __get_file_path():
        return os.path.dirname(os.path.abspath(__file__))
