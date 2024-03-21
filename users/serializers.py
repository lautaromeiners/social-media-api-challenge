from rest_framework import serializers
from .models import User


class BaseUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    followers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    following = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    token = serializers.CharField(read_only=True)

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    class Meta:
        model = User
        fields = ("username", "email", "followers", "following", "password", "token")


class UserDetailSerializer(BaseUserSerializer):
    posts_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    def get_posts_count(self, obj):
        return obj.posts.count()

    def get_comments_count(self, obj):
        return obj.comments.count()

    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + ("posts_count", "comments_count")
