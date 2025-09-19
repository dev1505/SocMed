from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import (
    FollowSerializer,
    GetUserFollowers_FollowingSerializer,
    UnFollowSerializer,
)
from .service import (
    follow_user_creation,
    follow_user_deletion,
    get_user_followers,
    get_user_followings,
)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def follow_user(request):
    serializer = FollowSerializer(data=request.data, context={"request": request})
    if serializer.is_valid():
        follow_user_creation(
            follower=serializer.data["follower"], following=serializer.data["following"]
        )

        return Response(
            {
                "message": "Followed successfully",
                "data": serializer.data,
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


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def unfollow_user(request):
    serializer = UnFollowSerializer(data=request.data, context={"request": request})
    if serializer.is_valid():
        follow_user_deletion(
            follower=serializer.data["follower"], following=serializer.data["following"]
        )

        return Response(
            {
                "message": "Unfollowed successfully",
                "data": serializer.data,
                "success": True,
            },
            status=status.HTTP_200_OK,
        )

    return Response(
        {
            "message": serializer.errors,
            "success": False,
        },
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_followers(request):
    followers = get_user_followers(request.user.id)
    serialized_followers = GetUserFollowers_FollowingSerializer(followers, many=True)
    return Response(
        {
            "message": "User followers",
            "data": serialized_followers.data,
            "success": True,
        },
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_followings(request):
    followers = get_user_followings(request.user.id)
    serialized_followers = GetUserFollowers_FollowingSerializer(followers, many=True)
    return Response(
        {
            "message": "User followers",
            "data": serialized_followers.data,
            "success": True,
        },
        status=status.HTTP_200_OK,
    )
