from django.test import TestCase

from accounts.models import User


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.username = "user"
        cls.password = "1234"
        cls.first_name = "test"
        cls.last_name = "test"

        cls.user = User.objects.create_superuser(
            username=cls.username,
            password=cls.password,
            first_name=cls.first_name,
            last_name=cls.last_name,
        )

    def test_user_has_information_fields(self):
        self.assertIsInstance(self.user.username, str)
        self.assertEqual(self.user.username, self.username)

        self.assertIsInstance(self.user.first_name, str)
        self.assertEqual(self.user.first_name, self.first_name)

        self.assertIsInstance(self.user.last_name, str)
        self.assertEqual(self.user.last_name, self.last_name)
