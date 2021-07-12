import unittest
import time
from unittest.mock import patch

from sentinel.oidc.token import Token


class TestToken(unittest.TestCase):

    @patch.object(time, "time")
    def test_is_expired(self, time_time):
        time_time.return_value = 1624546628
        token = Token(access_token="ac", expires_in=3600, refresh_token="rf", id_token="id")
        token.expires_at = 1624546528
        self.assertTrue(token.is_expired())

    @patch.object(time, "time")
    def test_is_expired_closely(self, time_time):
        time_time.return_value = 1624546628
        token = Token(access_token="ac", expires_in=3600, refresh_token="rf", id_token="id")
        token.expires_at = 1624546628
        self.assertTrue(token.is_expired())

    @patch.object(time, "time")
    def test_is_expired_within_expire_buffer_time(self, time_time):
        time_time.return_value = 1624546628
        token = Token(access_token="ac", expires_in=3600, refresh_token="rf", id_token="id")
        token.expires_at = 1624546630
        self.assertTrue(token.is_expired())

    @patch.object(time, "time")
    def test_is_not_expired(self, time_time):
        time_time.return_value = 1624546628
        token = Token(access_token="ac", expires_in=3600, refresh_token="rf", id_token="id")
        token.expires_at = 1624546629 + Token.EXPIRE_BUFFER
        self.assertFalse(token.is_expired())

    @patch.object(time, "time")
    def test_is_not_expired_wide_range(self, time_time):
        time_time.return_value = 1624546628
        token = Token(access_token="ac", expires_in=3600, refresh_token="rf", id_token="id")
        token.expires_at = 1624546728
        self.assertFalse(token.is_expired())

    @patch.object(time, "time")
    def test_expires_at(self, time_time):
        time_time.return_value = 1624543028
        token = Token(access_token="at", expires_in=3600, refresh_token="rf", id_token="id")
        token.renew_expires_at_from_now()
        self.assertEqual(1624546628, token.expires_at)
