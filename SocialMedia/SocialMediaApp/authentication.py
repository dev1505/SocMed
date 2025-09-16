from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


def validate_token(request):
    jwt_authenticator = JWTAuthentication()
    user_auth_tuple = jwt_authenticator.authenticate(request)
    if user_auth_tuple is None:
        raise AuthenticationFailed("Invalid or missing token.")
    user, validated_token = user_auth_tuple
    return user, validated_token
