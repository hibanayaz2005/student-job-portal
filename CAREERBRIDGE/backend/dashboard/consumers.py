import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

User = get_user_model()

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_anonymous:
            await self.close()
        else:
            self.group_name = f"user_notifications_{self.user.id}"
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_notification(self, event):
        await self.send(text_data=json.dumps(event["data"]))

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.peer_id = self.scope['url_route']['kwargs'].get('peer_id')
        
        if self.user.is_anonymous or not self.peer_id:
            await self.close()
        else:
            # Create a unique room name for the pair
            ids = [int(self.user.id), int(self.peer_id)]
            ids.sort()
            self.room_name = f"chat_{ids[0]}_{ids[1]}"
            await self.channel_layer.group_add(self.room_name, self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "room_name"):
            await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message")
        msg_type = data.get("type", "text")
        file_url = data.get("file_url", "")
        
        if message or file_url:
            # Save message to DB
            saved_msg = await self.save_message(message, msg_type, file_url)
            
            # Broadcast to group
            await self.channel_layer.group_send(
                self.room_name,
                {
                    "type": "chat_message",
                    "data": {
                        "id": saved_msg.id,
                        "sender_id": self.user.id,
                        "message": message,
                        "msg_type": msg_type,
                        "file_url": file_url,
                        "timestamp": saved_msg.created_at.strftime("%I:%M %p")
                    }
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event["data"]))

    @database_sync_to_async
    def save_message(self, text, msg_type, file_url):
        from mentorship.models import Message
        receiver = User.objects.get(id=self.peer_id)
        # Handle file upload verification logic if needed
        return Message.objects.create(
            sender=self.user,
            receiver=receiver,
            text=text if msg_type == 'text' else f"Shared a file: {file_url}"
        )

class AnalyticsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "platform_analytics"
        await self.channel_layer.group_add(self.group_name, self.channel_layer.name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_layer.name)

    async def platform_update(self, event):
        await self.send(text_data=json.dumps(event["data"]))