from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


class User(AbstractUser):
    followers = models.ManyToManyField(
        "self", symmetrical=False, blank=True, related_name="user_followers"
    )
    following = models.ManyToManyField(
        "self", symmetrical=False, blank=True, related_name="user_following"
    )

    def follow(self, other_user):
        if self.id == other_user.id:
            raise ValidationError("You cannot follow yourself.")
        self.following.add(other_user)
        other_user.followers.add(self)

    def unfollow(self, other_user):
        self.following.remove(other_user)
        other_user.followers.remove(self)
