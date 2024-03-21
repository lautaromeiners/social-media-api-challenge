from rest_framework import serializers
from users.serializers import BaseUserSerializer
from .models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    author = BaseUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ("author", "content", "created_at")


class PostSerializer(serializers.ModelSerializer):
    author = BaseUserSerializer(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = ("author", "content", "created_at", "comments")
