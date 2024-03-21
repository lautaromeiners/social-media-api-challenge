from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    followers = models.ManyToManyField(
        "self", symmetrical=False, blank=True, related_name="user_followers"
    )
    following = models.ManyToManyField(
        "self", symmetrical=False, blank=True, related_name="user_following"
    )
