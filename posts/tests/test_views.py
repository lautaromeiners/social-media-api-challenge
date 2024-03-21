from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from posts.models import Post, Comment


class PostListTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.client.force_authenticate(user=self.user)
        self.post1 = Post.objects.create(author=self.user, content="Test Post 1")
        self.post2 = Post.objects.create(author=self.user, content="Test Post 2")

    def test_post_list_authenticated(self):
        response = self.client.get(reverse("post-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)  # Check post count
        self.assertEqual(Post.objects.count(), 2)

    def test_post_list_unauthenticated(self):
        self.client.force_authenticate(user=None)  # Remove authentication
        response = self.client.get(reverse("post-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_create(self):
        self.assertEqual(Post.objects.count(), 2)
        data = {"content": "Test Post 3"}
        response = self.client.post(reverse("post-list"), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["content"], "Test Post 3")
        self.assertEqual(Post.objects.count(), 3)


class PostDetailTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.client.force_authenticate(user=self.user)
        self.post = Post.objects.create(author=self.user, content="Test Post")
        self.comment = Comment.objects.create(
            author=self.user, post=self.post, content="Test Comment 1"
        )

    def test_post_detail_authenticated(self):
        url = reverse("post-detail", kwargs={"pk": self.post.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["content"], self.post.content)
        self.assertEqual(
            response.data["comments"][0]["author"]["username"], self.user.username
        )
        self.assertEqual(response.data["comments"][0]["content"], self.comment.content)

    def test_post_detail_unauthenticated(self):
        self.client.force_authenticate(user=None)  # Remove authentication
        url = reverse("post-detail", kwargs={"pk": self.post.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_not_found(self):
        url = reverse("post-detail", kwargs={"pk": 100})  # Non-existent ID
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestCommentList(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.user2 = User.objects.create_user(
            username="othertestuser", password="otherpassword123"
        )
        self.client.force_authenticate(user=self.user1)
        self.post = Post.objects.create(author=self.user1, content="Test Post")
        self.comment1 = Comment.objects.create(
            author=self.user1, post=self.post, content="Test Comment 1"
        )
        self.comment2 = Comment.objects.create(
            author=self.user2, post=self.post, content="Test Comment 2"
        )

    def test_comment_list_authenticated(self):
        self.assertEqual(Comment.objects.count(), 2)
        url = reverse("comment-list", kwargs={"pk": self.post.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["author"]["username"], self.user1.username)
        self.assertEqual(response.data[0]["content"], self.comment1.content)
        self.assertEqual(response.data[1]["author"]["username"], self.user2.username)
        self.assertEqual(response.data[1]["content"], self.comment2.content)

    def test_comment_list_unauthenticated(self):
        self.client.force_authenticate(user=None)  # Remove authentication
        url = reverse("comment-list", kwargs={"pk": self.post.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_comment_create(self):
        url = reverse("comment-list", kwargs={"pk": self.post.pk})
        data = {"content": "Test Comment 3"}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["content"], "Test Comment 3")
