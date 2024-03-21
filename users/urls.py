from django.urls import path
from .views import UserList, UserDetail, UserCreate, UserFollow, UserUnfollow

urlpatterns = [
    path("", UserList.as_view(), name="user-list"),
    path("create/", UserCreate.as_view(), name="user-create"),
    path("<int:pk>/", UserDetail.as_view(), name="user-detail"),
    path(
        "<int:pk>/follow/<int:followee_pk>/", UserFollow.as_view(), name="user-follow"
    ),
    path(
        "<int:pk>/unfollow/<int:following_pk>/",
        UserUnfollow.as_view(),
        name="user-unfollow",
    ),
]
