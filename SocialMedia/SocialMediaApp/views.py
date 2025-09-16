from typing import Any

from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from SocialMediaApp.models import User
from SocialMediaApp.serializers import UserSerializer

# Create your views here.


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_deleted=False)
    serializer_class = UserSerializer

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return Response({"message": "Users", "data": self.queryset})
