from django.urls import reverse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from users.models import User
from users.serializers import UserSerializer
from users.views import UserList, UserDetail, UserCreate, UserFollow, UserUnfollow


class UserListTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.client.force_authenticate(user=self.user)

    def test_get_user_list_authenticated(self):
        url = reverse("user-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class UserDetailTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.client.force_authenticate(user=self.user)

    def test_get_user_detail_authenticated(self):
        url = reverse("user-detail", kwargs={"pk": self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.user.username)

    def test_get_user_detail_unauthenticated(self):
        url = reverse("user-detail", kwargs={"pk": self.user.pk})
        self.client.force_authenticate(user=None)  # Remove authentication
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserCreateTest(APITestCase):

    def test_create_user(self):
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "password456",
        }
        url = reverse("user-create")
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], data["username"])
        self.assertIn("token", response.data)  # Check token is included


class UserFollowTest(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password123")
        self.user2 = User.objects.create_user(username="user2", password="password456")
        self.client.force_authenticate(user=self.user1)

    def test_follow_user(self):
        url = reverse(
            "user-follow", kwargs={"pk": self.user1.pk, "followee_pk": self.user2.pk}
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user1.following.count(), 1)

    def test_follow_user_already_followed(self):
        self.user1.follow(self.user2)
        self.user1.save()
        url = reverse(
            "user-follow", kwargs={"pk": self.user1.pk, "followee_pk": self.user2.pk}
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # No error
        self.assertEqual(
            self.user1.following.count(), 1
        )  # And no change, following count remains 1


class UserUnfollowTest(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password123")
        self.user2 = User.objects.create_user(username="user2", password="password456")
        self.user1.follow(self.user2)
        self.user1.save()
        self.client.force_authenticate(user=self.user1)

    def test_unfollow_user(self):
        url = reverse(
            "user-unfollow", kwargs={"pk": self.user1.pk, "following_pk": self.user2.pk}
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user1.following.count(), 0)

    def test_unfollow_user_not_followed(self):
        # Unfollow a user that wasn't followed initially
        another_user = User.objects.create_user(
            username="another", password="password789"
        )
        url = reverse(
            "user-unfollow",
            kwargs={"pk": self.user1.pk, "following_pk": another_user.pk},
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # No error
        self.assertEqual(
            self.user1.following.count(), 1
        )  # Following count remains 1 (user2)
