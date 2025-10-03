from asgiref.sync import sync_to_async
from h11 import Request
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

# from .serializers import UserSerializer
from .models import User


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


@sync_to_async
def get_user_from_jwt(token_str) -> User:
    jwt_auth = JWTAuthentication()
    validated_token = jwt_auth.get_validated_token(token_str)
    user = jwt_auth.get_user(validated_token)
    return user


# def validate_token(request):
#     jwt_authenticator = JWTAuthentication()
#     user_auth_tuple = jwt_authenticator.authenticate(request)
#     if user_auth_tuple is None:
#         raise AuthenticationFailed("Invalid or missing token.")
#     user, validated_token = user_auth_tuple
#     return user, validated_token


def create_cookie(serializer):
    response = Response(
        {
            "message": "Tokens generated",
            "data": serializer.validated_data["user"],
            "success": True,
        },
        status=status.HTTP_200_OK,
    )
    response.set_cookie(
        key="access",
        value=serializer.validated_data["access"],
        httponly=True,
        secure=False,
        max_age=60 * 60,
        samesite="Lax",
        # path="/",
        # domain="localhost",
    )

    response.set_cookie(
        key="refresh",
        value=serializer.validated_data["refresh"],
        httponly=True,
        secure=False,
        max_age=60 * 60 * 24,
        samesite="Lax",
        # path="/",
        # domain="localhost",
    )

    return response


def create_refresh_cookie(serializer):
    response = Response(
        {
            "message": "Tokens generated",
            "success": True,
        },
        status=status.HTTP_200_OK,
    )

    response.set_cookie(
        key="access",
        value=serializer.validated_data["access"],
        httponly=True,
        secure=False,
        max_age=60 * 60,
        samesite="Lax",
        # path="/",
        # domain="localhost",
    )

    response.set_cookie(
        key="refresh",
        value=serializer.validated_data["refresh"],
        httponly=True,
        secure=False,
        max_age=60 * 60 * 24,
        samesite="Lax",
        # path="/",
        # domain="localhost",
    )

    return response


def remove_cookie():
    response = Response(
        {
            "message": "User Logout Successful",
            "success": True,
        },
        status=status.HTTP_200_OK,
    )

    response.delete_cookie(key="access")
    response.delete_cookie(key="refresh")
    return response
