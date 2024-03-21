from django.urls import path
from .views import UserList, UserDetail, CreateUser, FollowUser

urlpatterns = [
    path("", UserList.as_view(), name="user-list"),
    path("create/", CreateUser.as_view(), name="create-user"),
    path("<int:pk>/", UserDetail.as_view(), name="user-detail"),
    path("<int:pk>/follow/<int:folowee_pk>/", FollowUser.as_view(), name="user-follow"),
]
