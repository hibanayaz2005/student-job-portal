from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json


class ChatConsumer(AsyncWebsocketConsumer):
    """
    Real-time private chat between a student and a mentor.
    Room name: chat_<smaller_user_id>_<larger_user_id>
    This ensures both users join the same group regardless who connects first.
    """

    async def connect(self):
        self.user = self.scope.get("user")

        if not self.user or not self.user.is_authenticated:
            await self.close(code=4001)
            return

        # Get the other participant's user id from the URL query string
        # e.g. /ws/chat/?peer=5
        qs = self.scope.get("query_string", b"").decode()
        params = dict(p.split("=") for p in qs.split("&") if "=" in p)
        peer_id_str = params.get("peer", "")

        try:
            self.peer_id = int(peer_id_str)
        except (ValueError, TypeError):
            await self.close(code=4002)
            return

        # Consistent room name: smaller id first
        ids = sorted([self.user.id, self.peer_id])
        self.room_group_name = f"chat_{ids[0]}_{ids[1]}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        # Send message history so the user sees past messages on open
        history = await self.get_history(self.user.id, self.peer_id)
        await self.send(text_data=json.dumps({
            "event_type": "history",
            "messages": history
        }))

    async def disconnect(self, close_code):
        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            return

        message_text = data.get("message", "").strip()
        if not message_text:
            return

        # Persist to database
        saved = await self.save_message(self.user.id, self.peer_id, message_text)

        # Broadcast to the room group (both participants)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message_text,
                "sender_id": self.user.id,
                "sender_name": self.user.get_full_name() or self.user.username,
                "timestamp": saved.created_at.strftime("%H:%M") if saved else "",
                "event_type": "message"
            }
        )

    async def chat_message(self, event):
        """Handler called when a message is sent to this group."""
        await self.send(text_data=json.dumps({
            "event_type": "message",
            "message": event["message"],
            "sender_id": event["sender_id"],
            "sender_name": event.get("sender_name", ""),
            "timestamp": event.get("timestamp", ""),
        }))

    # ── DB helpers ──────────────────────────────────────────────────────────

    @database_sync_to_async
    def save_message(self, sender_id, receiver_id, text):
        from mentorship.models import Message
        from django.contrib.auth import get_user_model
        User = get_user_model()
        try:
            sender = User.objects.get(id=sender_id)
            receiver = User.objects.get(id=receiver_id)
            return Message.objects.create(sender=sender, receiver=receiver, text=text)
        except User.DoesNotExist:
            return None

    @database_sync_to_async
    def get_history(self, user_id, peer_id):
        from mentorship.models import Message
        from django.db.models import Q
        msgs = Message.objects.filter(
            (Q(sender_id=user_id) & Q(receiver_id=peer_id)) |
            (Q(sender_id=peer_id) & Q(receiver_id=user_id))
        ).order_by("created_at")[:100]

        return [
            {
                "sender_id": m.sender_id,
                "sender_name": m.sender.get_full_name() or m.sender.username,
                "message": m.text,
                "timestamp": m.created_at.strftime("%H:%M"),
            }
            for m in msgs
        ]