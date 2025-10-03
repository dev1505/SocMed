import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from SocialMediaApp.authentication import get_user_from_jwt
from SocialMediaApp.models import User
from django.db.models import Q
from .models import UserMessages
from .Serializers import UserMessageSerializer


def Home(request):
    return render(request, "websocketpage.html")


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        self.user = await get_user_from_jwt(token_str=self.scope["cookies"]["access"])
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)

        # Save message once
        await self.save_message(
            from_user_id=self.user.pk,
            to_user_id=data["to_user_id"],
            message=data["message"],
        )

        # Broadcast to the other user
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": data["message"],
                "to_user_id": data["to_user_id"],
                "from_user_id": self.user.pk,
            },
        )

    async def chat_message(self, event):
        # Only send to the other users
        if event["from_user_id"] == self.user.pk:
            return

        await self.send(
            text_data=json.dumps(
                {
                    "message": event["message"],
                    "user": event["from_user_id"],
                }
            )
        )

    @database_sync_to_async
    def save_message(self, from_user_id, to_user_id, message):
        from_user = User.objects.get(id=from_user_id)
        to_user = User.objects.get(id=to_user_id)
        return UserMessages.objects.create(
            from_user=from_user, to_user=to_user, message=message
        )


class Get_User_Messages(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, user_id: int, *args, **kwargs):
        user_messages = UserMessages.objects.filter(
            Q(from_user=request.user.pk, to_user=user_id)
            | Q(from_user=user_id, to_user=request.user.pk)
        ).order_by("message_time")

        serialized_messages = UserMessageSerializer(user_messages, many=True)

        return Response(
            {
                "data": serialized_messages.data,
                "success": True,
            },
            status=status.HTTP_200_OK,
        )
