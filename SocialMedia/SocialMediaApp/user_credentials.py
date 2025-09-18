from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (
    LoginSerializer,
    SignupSerializer,
    UserSerializer,
)
from rest_framework_simplejwt.tokens import AccessToken


@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request: Request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "User registered successfully"}, status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Login(TokenObtainPairView):
    serializer_class = LoginSerializer


def get_current_user(user):
    return UserSerializer(user).data
