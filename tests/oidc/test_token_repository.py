import unittest
from unittest.mock import patch

from sentinel.config.config_repository import ConfigRepository
from sentinel.oidc.token import Token
from sentinel.oidc.token_repository import TokenRepository


class TokenRepositoryTest(unittest.TestCase):

    @patch.object(ConfigRepository, "set")
    def test_set(self, config_repository_set_mock):
        token = Token(access_token="at", refresh_token="rf", id_token="id", expires_in=4711)

        repository = TokenRepository()
        repository.set(token)

        config_repository_set_mock.assert_called_with(token)

    @patch.object(ConfigRepository, "get")
    def test_get(self, config_repository_get_mock):
        expected = Token(access_token="at", refresh_token="rf", id_token="id", expires_in=4711)
        config_repository_get_mock.return_value = expected

        repository = TokenRepository()
        self.assertDictEqual(expected.__dict__, repository.get().__dict__)
