from urllib.parse import urlencode

import requests
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import SocialLoginSerializer


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter


class GoogleLoginURL(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        client_id = (
            settings.SOCIALACCOUNT_PROVIDERS.get("google", {})
            .get("APP", {})
            .get("client_id", None)
        )
        base_url = "https://accounts.google.com/o/oauth2/v2/auth"
        params = {
            "client_id": client_id,
            "redirect_uri": "http://127.0.0.1:8000/auth/google/callback/",
            "response_type": "code",
            "scope": "openid email profile",
            "access_type": "offline",
            "prompt": "consent",
        }
        url = f"{base_url}?{urlencode(params)}"
        return Response(
            {
                "data": url,
                "success": True,
            }
        )


class GoogleCallback(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        code = request.GET.get("code")
        if not code:
            return Response(
                {
                    "message": "No code provided",
                    "success": False,
                }
            )

        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "code": code,
            "client_id": settings.SOCIALACCOUNT_PROVIDERS["google"]["APP"]["client_id"],
            "client_secret": settings.SOCIALACCOUNT_PROVIDERS["google"]["APP"][
                "secret"
            ],
            "redirect_uri": "http://127.0.0.1:8000/auth/google/callback/",
            "grant_type": "authorization_code",
        }
        req = requests.post(token_url, data=data)
        tokens = req.json()
        access_token = tokens.get("access_token")
        if not access_token:
            return Response(
                {
                    "message": "Failed to retrieve access token",
                    "details": tokens,
                    "success": False,
                }
            )

        userinfo_url = "https://www.googleapis.com/oauth2/v3/userinfo"
        headers = {"Authorization": f"Bearer {access_token}"}
        userinfo_response = requests.get(userinfo_url, headers=headers)
        user_info = userinfo_response.json()

        serializer = SocialLoginSerializer(
            data={
                "email": user_info.get("email"),
                "username": user_info.get("name"),
                "auth_id": user_info.get("sub"),
                "auth_id_by": "google",
            }
        )
        serializer.is_valid(raise_exception=True)

        return Response(
            {
                "data": serializer.validated_data,
                "success": True,
            }
        )
