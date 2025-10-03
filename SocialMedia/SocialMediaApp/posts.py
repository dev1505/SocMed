from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post, User
from .serializers import GetPostSerializer, UserSerializer


class MessagePagination(LimitOffsetPagination):
    default_limit = 10


# class Get_Post(APIView):
#     permission_classes = [IsAuthenticated]
#     pagination_class = MessagePagination

#     def get(self, request: Request):
#         user = request.user
#         posts = Post.objects.exclude(user=user.pk).order_by("-created_at")

#         paginator = self.pagination_class()
#         page = paginator.paginate_queryset(posts, request)
#         serializer = GetPostSerializer(page, many=True, context={"request": request})

#         return Response(
#             {
#                 "data": serializer.data,
#                 "success": True,
#                 "count": paginator.count,  # total number of posts
#                 "next": paginator.get_next_link(),  # next page link
#                 "previous": paginator.get_previous_link(),  # prev page link
#             },
#             status=status.HTTP_200_OK,
#         )


class Get_Post(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        user = request.user
        posts = Post.objects.exclude(user=user.pk)
        serialized_posts = GetPostSerializer(
            posts, many=True, context={"request": request}
        )
        if not serialized_posts.data:
            return Response(
                {
                    "data": [],
                    "success": True,
                    "message": "No posts found",
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {
                "data": serialized_posts.data,
                "success": True,
            },
            status=status.HTTP_200_OK,
        )


class Get_User_Post(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        user = request.user
        posts = Post.objects.filter(user=user.pk)
        serialized_posts = GetPostSerializer(
            posts, many=True, context={"request": request}
        )
        user = User.objects.get(pk=user.pk)
        serialized_user = UserSerializer(user)
        print(serialized_user.data)
        if not serialized_posts.data or not serialized_user.data:
            return Response(
                {
                    "data": [],
                    "success": True,
                    "message": "No posts found",
                },
                status=status.HTTP_200_OK,
            )

        data = serialized_posts.data
        return Response(
            {
                "data": data,
                "success": True,
            },
            status=status.HTTP_200_OK,
        )


class Get_Other_Users_Post(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, *args, **kwargs):
        posts = Post.objects.filter(user=request.data.get("user_id"))
        serialized_posts = GetPostSerializer(
            posts, many=True, context={"request": request}
        )

        if not serialized_posts.data:
            return Response(
                {
                    "data": [],
                    "success": True,
                    "message": "No posts found",
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {
                "data": serialized_posts.data,
                "success": True,
            },
            status=status.HTTP_200_OK,
        )
