from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Followers, User
from .serializers import FollowSerializer, UserSerializer
from .user_credentials import get_current_user


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def follow_user(request: Request):
    current_user = get_current_user(request.user)
    serializer = FollowSerializer(data=request.data)
    print(current_user.get("id", None))
    remaning_users = User.objects.exclude(pk=current_user.get("id", None))
    serialized_remaining_user = UserSerializer(remaning_users, many=True)
    return Response(
        {
            "data": "this is following view",
            "user": current_user,
            "valid": serializer.is_valid(),
            "remaining_users": serialized_remaining_user.data,
        }
    )
