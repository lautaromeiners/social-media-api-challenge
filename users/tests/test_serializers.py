from rest_framework.test import APITestCase
from users.models import User
from users.serializers import BaseUserSerializer, UserDetailSerializer
from posts.models import Post, Comment


class BaseUserSerializerTest(APITestCase):

    def test_serialize_user(self):
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password123"
        )
        serializer = BaseUserSerializer(user)
        self.assertEqual(serializer.instance.username, "testuser")
        self.assertEqual(serializer.instance.email, "test@example.com")

    def test_create_user(self):
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "password456",
        }
        serializer = BaseUserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            self.assertEqual(user.username, "newuser")
            self.assertEqual(user.email, "new@example.com")
            self.assertTrue(
                user.check_password("password456")
            )  # Checks password is hashed

    def test_password_write_only(self):
        user = User.objects.create_user(username="testuser", password="password123")
        serializer = BaseUserSerializer(user)
        self.assertNotIn(
            "password", serializer.data
        )  # Password shouldn't be included in serialized output


class UserDetailSerializerTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password123"
        )
        self.post1 = Post.objects.create(author=self.user, content="Test Post 1")
        self.post2 = Post.objects.create(author=self.user, content="Test Post 2")
        self.comment1 = Comment.objects.create(
            author=self.user, post=self.post1, content="Test Comment 1"
        )
        self.comment2 = Comment.objects.create(
            author=self.user, post=self.post2, content="Test Comment 2"
        )

    def test_user_detail_serializer_with_posts_and_comments(self):
        serializer = UserDetailSerializer(self.user)
        self.assertEqual(serializer.instance.username, "testuser")
        self.assertEqual(serializer.instance.email, "test@example.com")
        self.assertEqual(serializer.data["posts_count"], 2)
        self.assertEqual(serializer.data["comments_count"], 2)

    def test_user_detail_serializer_without_posts_or_comments(self):
        new_user = User.objects.create_user(
            username="new_user", email="new_user@example.com", password="new_password"
        )
        serializer = UserDetailSerializer(new_user)
        self.assertEqual(serializer.instance.username, "new_user")
        self.assertEqual(serializer.instance.email, "new_user@example.com")
        self.assertEqual(serializer.data["posts_count"], 0)
        self.assertEqual(serializer.data["comments_count"], 0)
