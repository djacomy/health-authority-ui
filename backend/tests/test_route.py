import unittest


from tests.utils.mixins import BaseTest


class TestAuth(BaseTest):
    fixtures = ["users.json"]

    def test_routes(self):
        response = self.client.get("/routes")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
