from rest_framework.test import APITestCase

from accounts.models import User


class UserViewTest(APITestCase):
    def test_create_new_user(self):
        user_data = {
            "username": "user_test",
            "password": "1234",
            "first_name": "user",
            "last_name": "test",
            "is_superuser": False,
            "is_staff": False,
        }
        response = self.client.post("/api/accounts/", user_data)

        self.assertEqual(response.status_code, 201)

        self.assertEqual(response.json()["username"], "user_test")

    def test_create_user_with_wrong_body_on_request(self):
        user_data = {"username": "user"}

        response = self.client.post("/api/accounts/", **user_data)

        self.assertEqual(response.status_code, 422)

    def test_create_user_with_same_username(self):
        user_data_1 = {
            "username": "user_test",
            "password": "1234",
            "first_name": "user1",
            "last_name": "test",
            "is_superuser": False,
            "is_staff": False,
        }
        self.client.post("/api/accounts/", user_data_1)

        user_data_2 = {
            "username": "user_test",
            "password": "1234",
            "first_name": "user2",
            "last_name": "test",
            "is_superuser": False,
            "is_staff": False,
        }
        response = self.client.post("/api/accounts/", user_data_2)

        self.assertEqual(response.status_code, 422)


class LoginViewTest(APITestCase):
    def setUp(self):
        User.objects.create_user(
            username="user_test",
            password="1234",
            first_name="user",
            last_name="test",
            is_superuser=False,
            is_staff=False,
        )

    def test_login_success(self):
        login_data = {"username": "user_test", "password": "1234"}

        response = self.client.post("/api/login/", login_data)

        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json())

    def test_login_invalid_credentials(self):
        login_data = {"username": "user_test", "password": "12"}

        response = self.client.post("/api/login/", login_data)

        self.assertEqual(response.status_code, 401)

    def test_login_missing_fields(self):
        login_data = {"password": "123"}

        response = self.client.post("/api/login/", login_data)

        self.assertEqual(response.status_code, 400)
