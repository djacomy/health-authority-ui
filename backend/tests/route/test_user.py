import json
import unittest

from healthautority.model import User

from tests.utils.mixins import BaseTest, BaseAuthMixin


class TestAuth(BaseTest):
    fixtures = ["users.json"]

    def test_routes(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        params = {"email": "joe@example.fr", "password": "super-secret-password"}
        response = self.client.post("/api/auth/login", json=params, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data.decode("utf-8"))
        self.assertIn("token", result)


class TestUser(BaseAuthMixin, BaseTest):
    maxDiff = None
    fixtures = ["users.json"]

    def test_get_user_platfoem(self):

        token = self.authenticate("joe@example.fr", "super-secret-password")
        url = "api/users/1000"
        response = self.get(url, token)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(
            result,
            {
                "created_at": "2020-04-15T12:40:14.462544",
                "updated_at": "2020-04-15T12:40:14.462544",
                "id": 1000,
                "email": "joe@example.fr",
                "firstname": "joe",
                "lastname": "Leduc",
                "phone_number": "0123456799",
            },
        )

    def test_get_user_etablissement(self):
        token = self.authenticate("joe@example.fr", "super-secret-password")
        url = "api/users/1001"
        response = self.get(url, token)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(
            result,
            {
                "created_at": "2020-04-15T12:40:14.462544",
                "updated_at": "2020-04-15T12:40:14.462544",
                "id": 1001,
                "email": "mickael@example.fr",
                "firstname": "Michael",
                "lastname": "Tartempion",
                "phone_number": "0123456789",
            },
        )

    def test_update_user(self):
        token = self.authenticate("joe@example.fr", "super-secret-password")
        url = "api/users/1000"
        response = self.put(url, token, {"firstname": "titi", "lastname": "toto"})
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data.decode("utf-8"))

        for k, v in {"email": "joe@example.fr", "firstname": "titi", "id": 1000, "lastname": "toto"}.items():
            self.assertIn(k, result)
            self.assertEqual(result[k], v)

    def test_delete_user(self):
        token = self.authenticate("joe@example.fr", "super-secret-password")
        url = "api/users/1000"
        response = self.delete(url, token)
        self.assertEqual(response.status_code, 204)
        self.assertIsNone(User.query.filter_by(email="joe@example.fr").first())


if __name__ == "__main__":
    unittest.main()
