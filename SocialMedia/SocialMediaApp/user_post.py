from django.core.files.base import ContentFile
from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post, User
from .serializers import (
    GetPostByIdSerializer,
    GetPostSerializer,
    LikePostSerializer,
    PostSerializer,
)


class PostUploadAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def post(self, request, *args, **kwargs):
        user: User = request.user
        content = request.data.get("content", "")
        image = request.FILES.get("image")

        if not content and not image:
            return Response(
                {
                    "message": "No content or image provided",
                    "success": False,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            post = Post(user=user, content=content)
            post.save()

            if image:
                extension = image.name.split(".")[-1]
                image_path = f"post-images/{post.pk}.{extension}"
                post.image.save(image_path, ContentFile(image.read()), save=True)

        serializer = self.serializer_class(post)
        return Response(
            {
                "data": serializer.data,
                "success": True,
            },
            status=status.HTTP_201_CREATED,
        )


class DeletePostView(APIView):
    serializer_class = GetPostByIdSerializer

    def post(self, request, *args, **kwargs):
        user: User = request.user
        user_post = Post.objects.get(user_id=user.pk, pk=request.data.get("post_id"))
        if user_post:
            post = GetPostSerializer(user_post)
            return Response(
                {
                    "message": "Post Exits",
                    "data": post.data,
                    "success": True,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "message": "Post does not Exit",
                    "success": False,
                },
                status=status.HTTP_200_OK,
            )


class LikeUnlikePost(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LikePostSerializer

    def post(self, request, *args, **kwargs):
        user: User = request.user  # type: ignore
        post_id = request.data.get("post_id")

        if not post_id:
            return Response(
                {
                    "message": "post_id is required",
                    "success": False,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response(
                {
                    "message": "Post not found",
                    "success": False,
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        if post.liked_by.filter(id=user.pk).exists():
            post.liked_by.remove(user)
            action = "unliked"
        else:
            post.liked_by.add(user)
            action = "liked"

        return Response(
            {
                "message": action,
                "success": True,
            },
            status=status.HTTP_200_OK,
        )
