from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .authentication import create_cookie
from .models import Followers, User
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
                {
                    "message": "No refresh token provided",
                    "success": False,
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = self.get_serializer(data={"refresh": refresh_token})

        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response(
                {
                    "message": "Invalid refresh token",
                    "success": False,
                },
                status=status.HTTP_401_UNAUTHORIZED,
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

        # Followers = users who follow this user
        followers = Followers.objects.filter(following=user).values(
            "follower__id", "follower__username", "follower__profile_pic"
        )

        # Following = users this user follows
        following = Followers.objects.filter(follower=user).values(
            "following__id", "following__username", "following__profile_pic"
        )

        return Response(
            {
                "message": "User is Logged In",
                "data": {
                    **user_data,
                    "followers": len(list(followers)),
                    "following": len(list(following)),
                },
                "success": True,
            },
            status=status.HTTP_200_OK,
        )
