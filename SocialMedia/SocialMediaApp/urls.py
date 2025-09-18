from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .followers import follow_user
from .google_github_auth import (
    GithubCallback,
    GithubLoginURL,
    GoogleCallback,
    GoogleLogin,
    GoogleLoginURL,
    logout,
)
from .posts import create_post
from .user_credentials import Login, signup

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("login/", Login.as_view(), name="login"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/google/", GoogleLogin.as_view(), name="google_login"),
    path("auth/google/url/", GoogleLoginURL.as_view(), name="google_login_url"),
    path("auth/google/callback/", GoogleCallback.as_view(), name="google_callback_url"),
    path("auth/github/login/", GithubLoginURL.as_view()),
    path("auth/github/callback/", GithubCallback.as_view()),
    path("user/post/", create_post, name="user_posts"),
    path("user/logout/", logout, name="user_logout"),
    path("user/follow/", follow_user, name="user_followers"),
]
