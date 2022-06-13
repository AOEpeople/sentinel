import unittest
from unittest.mock import Mock, patch

from sentinel.config.config import Config
from sentinel.oidc.client import Client
from sentinel.oidc.http.authorization_code_handler import AuthorizationCodeHandler


class TestClient(unittest.TestCase):

    @patch('sentinel.oidc.client.OicClient')
    def test_authorize_client(self, oic_client_mock):
        # mocking
        client_id = "1"
        client_secret = "secret"
        expected_access_token = "test"

        oic_client_mock().client_id.return_value = client_id
        oic_client_mock().client_secret.return_value = client_secret
        oic_client_mock().request_info.return_value = '', '', {}, None
        oic_client_mock().request_and_return.return_value = {"access_token": expected_access_token}

        client = Client(
            client_id=client_id,
            client_secret=client_secret,
            issuer='issuer',
            scopes=["openid"],
            reset_http_handler=False,
        )

        # execute
        token = client.authorize_client()

        # assert
        oic_client_mock().request_info.assert_called_once()
        oic_client_mock().request_and_return.assert_called_once()
        self.assertEqual(token.access_token, expected_access_token)

    @patch('sentinel.oidc.client.OicClient')
    @patch('sentinel.oidc.http.authorization_code_handler.AuthorizationCodeHandler')
    @patch('webbrowser.open')
    @patch('sentinel.libs.helpers.print_info')
    def test_authorize_client_raises_exception_with_missing_session_state(
        self,
        helpers_call,
        web_browser_call,
        http_handler_mock,
        oic_client_mock
    ):
        # mocking
        auth_req_mock = Mock()
        auth_req_mock.request = Mock(return_value="https://login.url")
        oic_client_mock.construct_AuthorizationRequest.return_value = auth_req_mock

        helpers_call.return_value = None
        web_browser_call.return_value = True
        AuthorizationCodeHandler.is_done = True
        AuthorizationCodeHandler.state = None
        AuthorizationCodeHandler.code = 'code'

        client = Client(
            client_id="1",
            client_secret="secret",
            issuer="issuer",
            scopes=["openid"],
            reset_http_handler=False,
        )

        # execute
        with self.assertRaises(Exception):
            client.authorize_user()

    @patch('sentinel.oidc.client.OicClient')
    @patch('sentinel.oidc.http.authorization_code_handler.AuthorizationCodeHandler')
    @patch('webbrowser.open')
    @patch('sentinel.libs.helpers.print_info')
    def test_authorize_client_raises_exception_with_missing_session_code(
            self,
            helpers_call,
            web_browser_call,
            http_handler,
            oic_client_mock
    ):
        # mocking
        auth_req_mock = Mock()
        auth_req_mock.request = Mock(return_value="https://login.url")
        oic_client_mock.construct_AuthorizationRequest = Mock(return_value=auth_req_mock)

        helpers_call.return_value = None
        web_browser_call.return_value = True
        AuthorizationCodeHandler.is_done = True
        AuthorizationCodeHandler.state = 'state'
        AuthorizationCodeHandler.code = None

        client = Client(
            client_id="1",
            client_secret="secret",
            issuer="issuer",
            scopes=["openid"],
            reset_http_handler=False,
        )

        # execute
        with self.assertRaises(Exception):
            client.authorize_user()

    @patch('sentinel.oidc.client.OicClient')
    @patch('sentinel.oidc.http.authorization_code_handler.AuthorizationCodeHandler')
    @patch('webbrowser.open')
    @patch('sentinel.libs.helpers.print_info')
    def test_authorize_client_raises_exception_with_compromised_session_state(
            self,
            helpers_call,
            web_browser_call,
            http_handler,
            oic_client_mock
    ):
        # mocking
        auth_req_mock = Mock()
        auth_req_mock.request = Mock(return_value="https://login.url")
        oic_client_mock.construct_AuthorizationRequest = Mock(return_value=auth_req_mock)

        helpers_call.return_value = None
        web_browser_call.return_value = True
        AuthorizationCodeHandler.is_done = True
        AuthorizationCodeHandler.state = 'compromised'
        AuthorizationCodeHandler.code = 'code'

        client = Client(
            client_id="1",
            client_secret="secret",
            issuer="issuer",
            scopes=["openid"],
            reset_http_handler=False,
        )

        # execute
        with self.assertRaises(Exception):
            client.authorize_user()

    @patch('sentinel.oidc.client.OicClient')
    @patch('sentinel.oidc.client.rndstr')
    @patch('sentinel.oidc.http.authorization_code_handler.AuthorizationCodeHandler')
    @patch('webbrowser.open')
    @patch('sentinel.libs.helpers.print_info')
    def test_authorize_client_raises_exception_with_missing_id_token_in_token_response(
            self,
            helpers_call,
            web_browser_call,
            http_handler,
            random_str,
            oic_client_mock
    ):
        # mocking
        random_string = 'random'
        token_response = {
            'access_token': 'a',
            'refresh_token': 'r',
            'expires_in': 60
        }

        auth_req_mock = Mock()
        auth_req_mock.request = Mock(return_value="https://login.url")

        oic_client_mock.construct_AuthorizationRequest = Mock(return_value=auth_req_mock)
        oic_client_mock.do_access_token_request = Mock(return_value=token_response)

        helpers_call.return_value = None
        web_browser_call.return_value = True

        AuthorizationCodeHandler.is_done = True
        AuthorizationCodeHandler.code = 'code'
        AuthorizationCodeHandler.state = random_string
        random_str.return_value = random_string

        client = Client(
            client_id="1",
            client_secret="secret",
            issuer="issuer",
            scopes=["openid"],
            reset_http_handler=False,
        )

        # execute
        with self.assertRaises(Exception):
            client.authorize_user()

    @patch('sentinel.oidc.client.OicClient')
    @patch('sentinel.oidc.client.rndstr')
    @patch('sentinel.oidc.http.authorization_code_handler.AuthorizationCodeHandler')
    @patch('webbrowser.open')
    @patch('sentinel.libs.helpers.print_info')
    def test_authorize_client_raises_exception_with_compromised_id_token_nonce(
            self,
            helpers_call,
            web_browser_call,
            http_handler,
            random_str,
            oic_client_mock
    ):
        # mocking
        random_string = 'random'
        token_response = {
            'id_token': {'nonce': 'compromised'},
            'access_token': 'a',
            'refresh_token': 'r',
            'expires_in': 60
        }

        auth_req_mock = Mock()
        auth_req_mock.request = Mock(return_value="https://login.url")

        oic_client_mock().construct_AuthorizationRequest = Mock(return_value=auth_req_mock)
        oic_client_mock().do_access_token_request = Mock(return_value=token_response)

        helpers_call.return_value = None
        web_browser_call.return_value = True

        AuthorizationCodeHandler.is_done = True
        AuthorizationCodeHandler.code = 'code'
        AuthorizationCodeHandler.state = random_string
        random_str.return_value = random_string

        client = Client(
            client_id="1",
            client_secret="secret",
            issuer="issuer",
            scopes=["openid"],
            reset_http_handler=False,
        )

        # execute
        with self.assertRaises(Exception):
            client.authorize_user()

    @patch('sentinel.oidc.client.TokenRepository')
    @patch('sentinel.oidc.client.OicClient')
    @patch('sentinel.oidc.client.rndstr')
    @patch('sentinel.oidc.http.authorization_code_handler.AuthorizationCodeHandler')
    @patch('webbrowser.open')
    @patch('sentinel.oidc.client.ConfigRepository')
    @patch('sentinel.libs.helpers.print_info')
    def test_authorize_user_when_token_does_not_yet_exist(
            self,
            helpers_call,
            config_repository_mock,
            web_browser_call,
            http_handler,
            random_str,
            oic_client_mock,
            token_repository_mock
    ):
        # mocking
        expected_access_token = "test"
        random_string = "random"
        token_response = {
            'id_token': {'nonce': random_string},
            'access_token': expected_access_token,
            'refresh_token': 'r',
            'expires_in': 60
        }

        config_repository_mock.fetch.return_value = Config(
            "client",
            "secret",
            "http://issuer.host",
            ["openid"],
            ["httpbin.org"],
            4711,
            4711,
            4711,
            4711,
        )

        token_repository_mock().exists.return_value = False

        auth_req_mock = Mock()
        auth_req_mock.request = Mock(return_value="https://login.url")
        oic_client_mock().construct_AuthorizationRequest.return_value = auth_req_mock
        oic_client_mock().do_access_token_request.return_value = token_response

        helpers_call.return_value = None
        web_browser_call.return_value = True
        AuthorizationCodeHandler.state = random_string
        AuthorizationCodeHandler.code = 'code'
        AuthorizationCodeHandler.is_done = True
        random_str.return_value = random_string

        client = Client(
            client_id="1",
            client_secret="secret",
            issuer="issuer",
            scopes=["openid"],
            reset_http_handler=False,
        )

        # execute
        token = client.authorize_user()

        # assert
        self.assertEqual(token.access_token, expected_access_token)

    @patch('sentinel.oidc.client.TokenRepository')
    @patch('sentinel.oidc.client.OicClient')
    @patch('sentinel.libs.helpers.print_debug')
    def test_authorize_user_with_token_refresh_and_expired_token(
            self,
            helpers_call,
            oic_client_mock,
            token_repository_mock
    ):
        # mocking
        expected_access_token = "test"
        token_response = {
            'id_token': {'nonce': 'random'},
            'access_token': expected_access_token,
            'refresh_token': 'r',
            'expires_in': 60
        }

        token_repository_mock().token_exists.return_value = True
        oic_client_mock().do_access_token_refresh.return_value = token_response
        helpers_call.return_value = None

        client = Client(
            client_id="1",
            client_secret="secret",
            issuer="issuer",
            scopes=["openid"],
            use_cache=True,
            reset_http_handler=False,
        )

        # execute
        token = client.authorize_user()

        # assert
        self.assertEqual(token.access_token, expected_access_token)
        token_repository_mock().set.assert_called_once_with(token)

    @patch('sentinel.oidc.client.OicClient')
    @patch('sentinel.libs.helpers.print_debug')
    def test_authorize_user_with_token_refresh_raises_exception_with_missing_access_token_in_response(
            self,
            helpers_call,
            oic_client_mock
    ):
        # mocking
        token_response = {
            'id_token': {'nonce': 'random'},
            'refresh_token': 'r',
            'expires_in': 60
        }

        oic_client_mock().do_access_token_refresh = Mock(return_value=token_response)

        helpers_call.return_value = None

        client = Client(
            client_id="1",
            client_secret="secret",
            issuer="issuer",
            scopes=["openid"],
            use_cache=True,
            reset_http_handler=False,
        )

        # execution
        with self.assertRaises(Exception):
            client.authorize_user()

    @patch('sentinel.oidc.client.TokenRepository')
    @patch('sentinel.oidc.client.OicClient')
    @patch('sentinel.libs.helpers.print_debug')
    def test_authorize_user_with_token_refresh_raises_exception_with_missing_expires_in(
            self,
            helpers_call,
            oic_client_mock,
            token_repository_mock
    ):
        # mocking
        token_response = {
            'id_token': {'nonce': 'random'},
            'access_token': 'a',
            'refresh_token': 'r'
        }

        oic_client_mock().do_access_token_refresh = Mock(return_value=token_response)

        helpers_call.return_value = None

        token_repository_mock().token_exists = Mock(return_value=True)

        client = Client(
            client_id="1",
            client_secret="secret",
            issuer="issuer",
            scopes=["openid"],
            use_cache=True,
            reset_http_handler=False,
        )

        # execution
        with self.assertRaises(Exception):
            client.authorize_user()

    @patch('sentinel.oidc.client.TokenRepository')
    @patch('sentinel.oidc.client.OicClient')
    @patch('sentinel.libs.helpers.print_debug')
    @patch('sentinel.libs.helpers.print_info')
    def test_authorize_user_with_valid_existing_token(
            self,
            print_debug,
            print_info,
            oic_client_mock,
            token_repository_mock
    ):
        # mocking
        expected_access_token = "test"

        token_mock = Mock(
            access_token=expected_access_token,
            refresh_token='r',
            id_token='id',
            expires_in=69,
            expires_at=2319823
        )
        token_mock.is_expired = Mock(return_value=False)

        print_debug.return_value = None
        print_info.return_value = None

        token_repository_mock().token_exists.return_value = True
        token_repository_mock().get.return_value = token_mock

        client = Client(
            client_id="1",
            client_secret="secret",
            issuer="issuer",
            scopes=["openid"],
            use_cache=True,
            reset_http_handler=False,
        )

        # execute
        token = client.authorize_user()

        # assert
        self.assertEqual(token.access_token, expected_access_token)
        token_repository_mock().get.assert_called_once()
