from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .authentication import create_cookie
from .serializers import (
    LoginSerializer,
    SignupSerializer,
)


@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request: Request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "message": "User registered successfully",
                "success": True,
            },
            status=status.HTTP_201_CREATED,
        )
    return Response(
        {
            "message": serializer.errors,
            "success": True,
        },
        status=status.HTTP_400_BAD_REQUEST,
    )


class Login(TokenObtainPairView):
    serializer_class = LoginSerializer


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer

    def get(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh")

        if not refresh_token:
            return Response(
                {"error": "No refresh token provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data={"refresh": refresh_token})

        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response(
                {"error": "Invalid refresh token"}, status=status.HTTP_401_UNAUTHORIZED
            )

        response = create_cookie(serializer=serializer)
        return response
