import unittest

from server import server

server.config["TESTING"] = True


class BaseTest(unittest.TestCase):
    app = server

    def setUp(self):
        self.client = server.test_client()

