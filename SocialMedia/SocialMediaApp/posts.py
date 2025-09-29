from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post
from .serializers import GetPostSerializer


class Get_Post(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        user = request.user
        posts = Post.objects.exclude(user=user.pk)
        serialized_posts = GetPostSerializer(posts, many=True)
        if serialized_posts.data:
            return Response(
                {
                    "data": serialized_posts.data,
                    "success": True,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "message": serialized_posts.errors,
                    "success": False,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
