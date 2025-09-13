from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .user_credentials import Login, signup

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("login/", Login.as_view(), name="login"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
