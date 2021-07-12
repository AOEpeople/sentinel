import filecmp
import json
import os
import shutil
import unittest

from sentinel.config.config_repository import ConfigRepository
from tests.config.fixtures.dummy import Dummy


class ConfigRepositoryTest(unittest.TestCase):
    def test_creates_dir(self):
        ConfigRepository(".test")
        self.assertTrue(os.path.isdir(".test"))

    def test_set_creates_file(self):
        dummy = Dummy("test", 472, ["a", "b"])

        repo = ConfigRepository(".test")
        repo.set(dummy)

        self.assertTrue(os.path.isfile(".test/dummy"))

    def test_set_contains_valid_json(self):
        dummy = Dummy("test", 472, ["a", "b"])

        repo = ConfigRepository(".test")
        repo.set(dummy)

        expected_file = open(os.path.realpath(os.path.dirname(os.path.abspath(__file__)) + "/fixtures/dummy.json"))
        expected = json.loads(expected_file.read())
        expected_file.close()

        actual_file = open(".test/dummy")
        actual = json.loads(actual_file.read())
        actual_file.close()

        self.assertEqual(expected, actual)

    def test_get(self):
        dummy = Dummy("test", 472, ["a", "b"])

        repo = ConfigRepository(".test")
        repo.set(dummy)

        self.assertEqual(type(repo.get(Dummy)), Dummy)
        self.assertEqual(dummy.__dict__, repo.get(Dummy).__dict__)

    def test_not_exists(self):
        repo = ConfigRepository(".test")

        self.assertFalse(repo.exists(Dummy))

    def test_exists(self):
        dummy = Dummy("test", 472, ["a", "b"])

        repo = ConfigRepository(".test")
        repo.set(dummy)

        self.assertTrue(repo.exists(Dummy))

    def tearDown(self):
        shutil.rmtree(".test")
