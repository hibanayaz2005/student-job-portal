from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_group_name = "mentor_chat"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message", "")
        sender_id = data.get("sender_id", "unknown")

        # Broadcast the student's message to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender_id": sender_id,
                "event_type": "message"
            }
        )

        # AI Bot Logic: If student sends a message, have the mentor reply automatically
        if sender_id == "student":
            asyncio.create_task(self.send_bot_reply(message))

    async def send_bot_reply(self, student_message):
        # Premium feel: Simulate thinking delay
        await asyncio.sleep(1.2)
        
        # Determine response based on input
        reply = "That's very interesting! I'm reviewing your career history to give you the best advice possible. Could you tell me more about your specific goal?"
        
        msg_lower = student_message.lower()
        if "resume" in msg_lower:
            reply = "I've reviewed your resume score. It's solid, but we can boost it! I recommend adding more specific metrics to your project descriptions, like 'improved performance by 30%'."
        elif "hi" in msg_lower or "hello" in msg_lower:
            reply = "Hello! I'm Dr. Ravi Patil. I'm here to help you navigate your career path. What's on your mind today?"
        elif "job" in msg_lower or "placement" in msg_lower:
            reply = "Placement season is a great time! With your current skill set, I'd suggest focusing on specialized roles in your branch. Have you checked the latest job postings in the portal?"
        elif "project" in msg_lower:
            reply = "Projects are the best way to show your skills! I'd recommend building a full-stack application that solves a real-world problem. Have you considered any specifically?"

        # Broadcast the mentor's auto-reply
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": reply,
                "sender_id": "mentor",
                "event_type": "message"
            }
        )

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender_id": event["sender_id"],
            "event_type": event["event_type"]
        }))