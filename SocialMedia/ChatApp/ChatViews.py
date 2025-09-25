import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.shortcuts import render
from SocialMediaApp.authentication import get_user_from_jwt
from SocialMediaApp.models import User

from .models import UserMessages


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
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": data["message"],
                "to_user_id": data["to_user_id"],
                "from_user_id": self.user.pk,
            },  # type: ignore
        )

    async def chat_message(self, event):
        try:
            await self.save_message(
                from_user_id=event["from_user_id"],
                to_user_id=event["to_user_id"],
                message=event["message"],
            )
        except Exception as e:
            raise e
        await self.send(
            text_data=json.dumps(
                {
                    "message": event["message"],
                    "user": self.user.username,
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
