from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .google_auth import GoogleCallback, GoogleLogin, GoogleLoginURL
from .user_credentials import Login, signup

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("login/", Login.as_view(), name="login"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/google/", GoogleLogin.as_view(), name="google_login"),
    path("auth/google/url/", GoogleLoginURL.as_view(), name="google_login_url"),
    path("auth/google/callback/", GoogleCallback.as_view(), name="google_callback_url"),
]
