from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .authentication import create_cookie
from .models import User
from .serializers import (
    LoginSerializer,
    SignupSerializer,
    get_current_user,
)


class SignupView(APIView):
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(self, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "User registered successfully",
                    "success": True,
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {
                    "message": serializer.errors,
                    "success": False,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class Login(TokenObtainPairView, APIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)  # type: ignore
        if serializer.is_valid():
            return create_cookie(serializer=serializer)
        return Response(
            {
                "message": serializer.errors,
                "success": False,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


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


class AuthChecking(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        user_id = request.query_params.get("user_id")
        if user_id:
            user = User.objects.get(pk=user_id)
        else:
            user = request.user
        user_data = get_current_user(user)
        return Response(
            {
                "message": "User is Logged In",
                "data": user_data,
                "success": True,
            },
            status=status.HTTP_200_OK,
        )
