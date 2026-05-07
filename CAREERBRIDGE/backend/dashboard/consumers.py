import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.core.cache import cache

User = get_user_model()

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_anonymous:
            await self.close()
        else:
            self.group_name = f"user_notifications_{self.user.id}"
            self.broadcast_group = "global_presence"
            
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.channel_layer.group_add(self.broadcast_group, self.channel_name)
            await self.accept()
            
            # Track in cache
            cache.set(f"user_online_{self.user.id}", True, timeout=86400)
            
            # Broadcast presence
            await self.channel_layer.group_send(
                self.broadcast_group,
                {
                    "type": "presence_update",
                    "data": {
                        "user_id": self.user.id,
                        "status": "online"
                    }
                }
            )

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
            await self.channel_layer.group_discard(self.broadcast_group, self.channel_name)
            
            # Remove from cache
            cache.delete(f"user_online_{self.user.id}")
            
            # Broadcast offline
            await self.channel_layer.group_send(
                self.broadcast_group,
                {
                    "type": "presence_update",
                    "data": {
                        "user_id": self.user.id,
                        "status": "offline"
                    }
                }
            )

    async def send_notification(self, event):
        await self.send(text_data=json.dumps(event["data"]))

    async def presence_update(self, event):
        # Only send to other users
        if event["data"]["user_id"] != self.user.id:
            await self.send(text_data=json.dumps({
                "type": "presence",
                "user_id": event["data"]["user_id"],
                "status": event["data"]["status"]
            }))

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
            
            # Send history
            history = await self.get_chat_history()
            await self.send(text_data=json.dumps({
                'event_type': 'history',
                'messages': history
            }))

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
                    "event_type": "message",
                    "id": saved_msg.id,
                    "sender_id": self.user.id,
                    "message": message,
                    "msg_type": msg_type,
                    "file_url": file_url,
                    "timestamp": saved_msg.created_at.strftime("%I:%M %p")
                }
            )
            
            # Notify peer
            await self.notify_peer(message, msg_type)

    async def chat_message(self, event):
        # We send the whole event (which now includes event_type)
        data = event.copy()
        data.pop('type') # remove the internal channels 'type'
        await self.send(text_data=json.dumps(data))

    async def notify_peer(self, message, msg_type):
        from dashboard.models import Notification
        from django.core.mail import send_mail
        from django.conf import settings
        
        sender_name = self.user.get_full_name() or self.user.username
        title = f"New Message from {sender_name}"
        body = message if msg_type == 'text' else "Sent an attachment."
        
        # Create dashboard notification
        await database_sync_to_async(Notification.objects.create)(
            user_id=self.peer_id,
            title=title,
            message=body
        )
        
        is_online = cache.get(f"user_online_{self.peer_id}")
        
        # WebSocket notification
        await self.channel_layer.group_send(
            f"user_notifications_{self.peer_id}",
            {
                "type": "send_notification",
                "data": {
                    "type": "new_message",
                    "title": title,
                    "message": body,
                    "sender_id": self.user.id,
                    "sender_name": sender_name,
                    "open_chat": True if is_online else False
                }
            }
        )
        
        # Email if offline
        if not is_online:
            await self.send_offline_email(self.peer_id, title, body)

    @database_sync_to_async
    def send_offline_email(self, peer_id, title, body):
        from django.core.mail import send_mail
        from django.conf import settings
        try:
            peer = User.objects.get(id=peer_id)
            if peer.email:
                send_mail(
                    title,
                    body,
                    settings.DEFAULT_FROM_EMAIL,
                    [peer.email],
                    fail_silently=True,
                )
        except Exception as e:
            print("Error sending offline chat email:", e)

    @database_sync_to_async
    def get_chat_history(self):
        from mentorship.models import Message
        from django.db.models import Q
        # Get last 50 messages between these two users
        msgs = Message.objects.filter(
            (Q(sender=self.user) & Q(receiver_id=self.peer_id)) |
            (Q(sender_id=self.peer_id) & Q(receiver=self.user))
        ).order_by('created_at')[:50]
        
        return [
            {
                'id': m.id,
                'sender_id': m.sender_id,
                'message': m.text,
                'timestamp': m.created_at.strftime("%I:%M %p")
            } for m in msgs
        ]

    @database_sync_to_async
    def save_message(self, text, msg_type, file_url):
        from mentorship.models import Message
        try:
            receiver = User.objects.get(id=self.peer_id)
            return Message.objects.create(
                sender=self.user,
                receiver=receiver,
                text=text if msg_type == 'text' else f"Shared a file: {file_url}"
            )
        except User.DoesNotExist:
            return None

class AnalyticsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "platform_analytics"
        await self.channel_layer.group_add(self.group_name, self.channel_layer.name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_layer.name)

    async def platform_update(self, event):
        await self.send(text_data=json.dumps(event["data"]))