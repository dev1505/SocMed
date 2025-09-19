from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


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
            "message": serializer.validated_data,
            "success": True,
        },
        status=status.HTTP_200_OK,
    )

    response.set_cookie(
        key="access",
        value=serializer.validated_data["access"],
        httponly=True,
        secure=True,
        max_age=60 * 60,
    )

    response.set_cookie(
        key="refresh",
        value=serializer.validated_data["refresh"],
        httponly=True,
        secure=True,
        max_age=60 * 60 * 24,
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
