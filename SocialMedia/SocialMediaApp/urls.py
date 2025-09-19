from django.urls import path

from .followers import follow_user, get_followers, unfollow_user
from .google_github_auth import (
    GithubCallback,
    GithubLoginURL,
    GoogleCallback,
    GoogleLoginURL,
    logout,
)
from .posts import create_post
from .user_credentials import CustomTokenRefreshView, Login, signup

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("login/", Login.as_view(), name="login"),
    path("user/logout/", logout, name="user_logout"),
    path("api/token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    # path("auth/google/", GoogleLogin.as_view(), name="google_login"),
    path("auth/google/login/", GoogleLoginURL.as_view(), name="google_login_url"),
    path("auth/google/callback/", GoogleCallback.as_view(), name="google_callback_url"),
    path("auth/github/login/", GithubLoginURL.as_view()),
    path("auth/github/callback/", GithubCallback.as_view()),
    path("user/post/", create_post, name="user_posts"),
    path("user/follow/", follow_user, name="user_follower"),
    path("user/unfollow/", unfollow_user, name="user_unfollow"),
    path("user/getfollowers/", get_followers, name="user_get_followers"),
    path("user/getfollowings/", get_followers, name="user_get_followers"),
]
