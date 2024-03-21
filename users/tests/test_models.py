from django.test import TestCase
from users.models import User
from django.core.exceptions import ValidationError


class UserTest(TestCase):

    def test_user_creation(self):
        user = User.objects.create_user(username="testuser", password="password123")
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.is_active)

    def test_follow_user(self):
        user1 = User.objects.create_user(username="user1", password="password123")
        user2 = User.objects.create_user(username="user2", password="password456")

        self.assertEqual(user1.following.count(), 0)
        user1.follow(user2)

        self.assertEqual(user1.following.count(), 1)
        self.assertEqual(user2.followers.count(), 1)

        # Because the relationship is not symmetrical user2 does not follow user1
        self.assertEqual(user2.following.count(), 0)

    def test_unfollow_user(self):
        user1 = User.objects.create_user(username="user1", password="password123")
        user2 = User.objects.create_user(username="user2", password="password456")

        user1.follow(user2)
        user1.unfollow(user2)

        self.assertEqual(user1.following.count(), 0)
        self.assertEqual(user2.followers.count(), 0)

    def test_following_doesnt_follow_self(self):
        user = User.objects.create_user(username="user", password="password123")
        with self.assertRaises(ValidationError):
            user.follow(user)
