# views.py
import rest_framework.status as status
from django.core.files.base import ContentFile
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from .models import User
from .serializers import UserAvatarSerializer


class ProfileUploadView(generics.GenericAPIView):
    serializer_class = UserAvatarSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, *args, **kwargs):
        user: User = request.user  # type:ignore
        file_obj = request.FILES.get("profile_pic")
        if not file_obj:
            return Response({"error": "No file uploaded"}, status=400)

        image_path = f"profile-pic/{user.pk}.{file_obj.name.split('.')[-1]}"

        try:
            if user.profile_pic:
                user.profile_pic.delete(save=False)
            user.profile_pic.save(
                image_path,
                ContentFile(file_obj.read()),
                save=True,
            )
            serializer = self.get_serializer(user)
            return Response(
                {
                    "data": serializer.data,
                    "success": True,
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response(
                {
                    "message": str(e),
                    "success": False,
                },
                status=status.HTTP_501_NOT_IMPLEMENTED,
            )
