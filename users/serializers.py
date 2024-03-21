from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    followers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    following = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "followers", "following", "password", "token")
