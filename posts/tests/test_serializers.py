from django.test import TestCase
from rest_framework import serializers

from users.models import User
from posts.models import Post, Comment
from posts.serializers import CommentSerializer, PostSerializer


class CommentSerializerTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="user1")
        self.post = Post.objects.create(author=self.user, content="Test Post 1")

    def test_comment_serializer(self):
        data = {"author": self.user, "content": "Test comment"}
        serializer = CommentSerializer(data=data)
        self.assertTrue(serializer.is_valid())


class PostSerializerTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="user1")

    def test_post_serializer(self):
        data = {"author": self.user, "content": "Test post"}
        serializer = PostSerializer(data=data)
        self.assertTrue(serializer.is_valid())
