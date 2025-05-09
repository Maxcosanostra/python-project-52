from django.urls import path
from .views import (
    UserListView,
    UserCreateView,
    UserUpdateView,
    UserDeleteView,
    LoginView,
    LogoutView,
)

urlpatterns = [
    path("users/", UserListView.as_view(), name="user_list"),
    path("users/create/", UserCreateView.as_view(), name="user_create"),
    path(
        "users/<int:pk>/update/", UserUpdateView.as_view(), name="user_update"
    ),
    path(
        "users/<int:pk>/delete/", UserDeleteView.as_view(), name="user_delete"
    ),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
