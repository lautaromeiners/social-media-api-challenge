from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import User
from .serializers import BaseUserSerializer, UserDetailSerializer


class UserList(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = BaseUserSerializer


class UserDetail(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer


class UserCreate(CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = BaseUserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        serializer.validated_data["token"] = token.key
        return super().perform_create(serializer)


class UserFollow(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, followee_pk):
        followee = get_object_or_404(User, pk=followee_pk)
        follower = request.user
        follower.follow(followee)
        follower.save()
        return Response(status=status.HTTP_200_OK)


class UserUnfollow(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, following_pk):
        following = get_object_or_404(User, pk=following_pk)
        follower = request.user
        follower.unfollow(following)
        follower.save()
        return Response(status=status.HTTP_200_OK)
