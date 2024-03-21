from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from rest_framework import status
from rest_framework.generics import (
    RetrieveAPIView,
    CreateAPIView,
    ListCreateAPIView,
    RetrieveDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .filters import PostFilter


class PostPagination(PageNumberPagination):
    page_size = 20
    page_query_param = "page"
    max_page_size = 100


class PostList(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    pagination_class = PostPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = PostFilter

    def get_queryset(self):
        queryset = (
            Post.objects.select_related("author")
            .prefetch_related(
                Prefetch("comments", queryset=Comment.objects.order_by("-created_at"))
            )
            .order_by("-created_at")
        )
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetail(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.select_related("author").prefetch_related("comments")
    serializer_class = PostSerializer

    def get_object(self):
        pk = self.kwargs.get("pk")
        post = get_object_or_404(self.queryset, pk=pk)
        post.comments.set(post.comments.order_by("-created_at")[:3])
        return post


class CommentList(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs.get("pk")
        queryset = Comment.objects.select_related("author", "post")
        return queryset.filter(post_id=post_id)

    def perform_create(self, serializer):
        pk = self.kwargs.get("pk")
        post = get_object_or_404(Post, pk=pk)
        serializer.save(author=self.request.user, post=post)
