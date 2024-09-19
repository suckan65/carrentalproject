from django.urls import path
from users.api import views

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path((""), views.UserListAPIView.as_view(), name="user-personal"),
    path(("auth/all/"), views.UserListAPIView.as_view(), name="user-all"),
    path(("auth/pages/"), views.UserListAPIView.as_view(), name="user-page-all"),
    path(("<int:pk>/auth/"), views.UserDetailAPIView.as_view(), name="user-detail-auth"),
    path(("auth/"), views.ChangePasswordView.as_view(), name="change-password"),
]









