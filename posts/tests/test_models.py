from django.test import TestCase
from posts.models import Post, Comment
from users.models import User
from django.core.exceptions import ValidationError


class PostTest(TestCase):

    def test_post_creation(self):
        user = User.objects.create_user(username="testuser", password="password123")
        post = Post.objects.create(author=user, content="This is a test post")
        self.assertEqual(post.content, "This is a test post")
        self.assertEqual(post.author, user)


class CommentTest(TestCase):

    def test_comment_creation(self):
        user = User.objects.create_user(username="testuser", password="password123")
        post = Post.objects.create(author=user, content="This is a test post")
        comment = Comment.objects.create(
            author=user, post=post, content="This is a test comment"
        )
        self.assertEqual(comment.content, "This is a test comment")
        self.assertEqual(comment.author, user)
        self.assertEqual(comment.post, post)
