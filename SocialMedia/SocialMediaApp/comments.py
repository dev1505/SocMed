import rest_framework.status as status
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.views import APIView

from .models import Comment, Post
from .serializers import (
    CommentSerializer,
    DeleteCommentSerializer,
    GetCommentsSerializer,
)


class AddCommentView(APIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def post(self, request, *args, **kwargs):
        post_id = request.data.get("post")
        content = request.data.get("content")

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response(
                {
                    "message": "Post not found",
                    "success": False,
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.serializer_class(
            data={"user": request.user.id, "post": post_id, "content": content}
        )
        if serializer.is_valid():
            commment = Comment.objects.create(
                user=request.user,
                post=post,
                content=content,
            )
            get_comment = GetCommentsSerializer(commment)
            return Response(
                {
                    "message": "Comment posted",
                    "data": get_comment.data,
                    "success": True,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {
                "message": serializer.errors,
                "success": False,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class DeleteCommentView(APIView):
    serializer_class = DeleteCommentSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def post(self, request, *args, **kwargs):
        comment_id = request.data.get("comment_id")
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response(
                {
                    "message": "Comment not found",
                    "success": False,
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        if (
            comment.post.user.id == request.user.id
            or comment.user.id == request.user.id
        ):
            comment.delete()
            return Response(
                {"message": "Comment deleted", "success": True},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "message": "You cannot delete this comment",
                    "success": False,
                },
                status=status.HTTP_403_FORBIDDEN,
            )


class GetCommentsView(APIView):
    serializer_class = GetCommentsSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def post(self, request, *args, **kwargs):
        post_id = request.data.get("post")

        comments = Comment.objects.filter(post_id=post_id)

        if not comments.exists():
            return Response(
                {
                    "message": "Comments not found",
                    "data": [],
                    "success": True,
                },
                status=status.HTTP_200_OK,
            )

        serializer = self.serializer_class(comments, many=True)
        return Response(
            {
                "data": serializer.data,
                "success": True,
            },
            status=status.HTTP_200_OK,
        )
