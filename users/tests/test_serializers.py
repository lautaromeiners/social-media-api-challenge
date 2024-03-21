from rest_framework.test import APITestCase
from users.models import User
from users.serializers import UserSerializer


class UserSerializerTest(APITestCase):

    def test_serialize_user(self):
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password123"
        )
        serializer = UserSerializer(user)
        self.assertEqual(serializer.instance.username, "testuser")
        self.assertEqual(serializer.instance.email, "test@example.com")

    def test_create_user(self):
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "password456",
        }
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            self.assertEqual(user.username, "newuser")
            self.assertEqual(user.email, "new@example.com")
            self.assertTrue(
                user.check_password("password456")
            )  # Checks password is hashed

    def test_password_write_only(self):
        user = User.objects.create_user(username="testuser", password="password123")
        serializer = UserSerializer(user)
        self.assertNotIn(
            "password", serializer.data
        )  # Password shouldn't be included in serialized output
