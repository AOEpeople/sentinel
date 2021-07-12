import os
import unittest
from unittest.mock import patch

from sentinel.oidc.proxy import Proxy


class ProxyTest(unittest.TestCase):

    @patch("sentinel.oidc.proxy.mitmdump")
    def test_run(self, mock):
        proxy = Proxy(
            port=4711,
            client_id="client",
            client_secret="secret",
            scopes=["openid"],
            issuer="http://test.issuer"
        )

        proxy.run()

        path = os.path.realpath(os.path.dirname(os.path.abspath(__file__)) + "../../../sentinel/oidc")

        mock.assert_called_with([
            '-s',
            f'{path}/mitmproxy/authorization.py',
            '--set',
            'authorization_context=user',
            '--set',
            'authorization_client_id=client',
            '--set',
            'authorization_client_secret=secret',
            '--set',
            'authorization_scopes=["openid"]',
            '--set',
            'authorization_issuer=http://test.issuer',
            '--set',
            'listen_port=4711',
            '--quiet',
        ])

    @patch("sentinel.oidc.proxy.mitmdump")
    def test_run_with_hosts(self, mock):
        proxy = Proxy(
            port=4711,
            client_id="client",
            client_secret="secret",
            scopes=["openid"],
            issuer="http://test.issuer",
            hosts=["valid1.host", "valid2.host"]
        )

        proxy.run()

        path = os.path.realpath(os.path.dirname(os.path.abspath(__file__)) + "../../../sentinel/oidc")

        mock.assert_called_with([
            '-s',
            f'{path}/mitmproxy/authorization.py',
            '--set',
            'authorization_context=user',
            '--set',
            'authorization_client_id=client',
            '--set',
            'authorization_client_secret=secret',
            '--set',
            'authorization_scopes=["openid"]',
            '--set',
            'authorization_issuer=http://test.issuer',
            '--set',
            'authorization_hosts=["valid1.host", "valid2.host"]',
            '--allow-hosts',
            '^.*valid1.host:80$',
            '--allow-hosts',
            '^.*valid1.host:443$',
            '--allow-hosts',
            '^.*valid2.host:80$',
            '--allow-hosts',
            '^.*valid2.host:443$',
            '--set',
            'listen_port=4711',
            '--quiet',
        ])

    @patch("sentinel.oidc.proxy.mitmdump")
    def test_run_with_cmd(self, mock):
        proxy = Proxy(
            port=4711,
            client_id="client",
            client_secret="secret",
            scopes=["openid"],
            issuer="http://test.issuer",
            cmd=["/bin/bash", "echo", "test"]
        )

        proxy.run()

        path = os.path.realpath(os.path.dirname(os.path.abspath(__file__)) + "../../../sentinel/oidc")

        mock.assert_called_with([
            '-s',
            f'{path}/mitmproxy/executor.py',
            '--set',
            'executor_cmd=["/bin/bash", "echo", "test"]',
            '-s',
            f'{path}/mitmproxy/authorization.py',
            '--set',
            'authorization_context=user',
            '--set',
            'authorization_client_id=client',
            '--set',
            'authorization_client_secret=secret',
            '--set',
            'authorization_scopes=["openid"]',
            '--set',
            'authorization_issuer=http://test.issuer',
            '--set',
            'listen_port=4711',
            '--quiet',
        ])

    @patch("sentinel.oidc.proxy.mitmdump")
    def test_run_with_context_client(self, mock):
        proxy = Proxy(
            port=4711,
            client_id="client",
            client_secret="secret",
            scopes=["openid"],
            issuer="http://test.issuer",
            context=Proxy.CONTEXT_CLIENT
        )

        proxy.run()

        path = os.path.realpath(os.path.dirname(os.path.abspath(__file__)) + "../../../sentinel/oidc")

        mock.assert_called_with([
            '-s',
            f'{path}/mitmproxy/authorization.py',
            '--set',
            'authorization_context=client',
            '--set',
            'authorization_client_id=client',
            '--set',
            'authorization_client_secret=secret',
            '--set',
            'authorization_scopes=["openid"]',
            '--set',
            'authorization_issuer=http://test.issuer',
            '--set',
            'listen_port=4711',
            '--quiet',
        ])

    @patch("sentinel.oidc.proxy.mitmdump")
    def test_run_with_unknown_context(self, mock):
        proxy = Proxy(
            port=4711,
            client_id="client",
            client_secret="secret",
            scopes=["openid"],
            issuer="http://test.issuer",
            context="unknown"
        )

        proxy.run()

        self.assertRaises(Exception)
