from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio
import random
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope.get("user")
        
        if self.user and self.user.is_authenticated:
            self.room_group_name = f"user_{self.user.id}_chat"
        else:
            session = self.scope.get("session")
            session_key = session.session_key if session else "anonymous"
            self.room_group_name = f"session_{session_key}_chat"

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
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            return

        message_text = data.get("message", "")
        sender_id = data.get("sender_id", "unknown")
        mentor_id = data.get("receiver_id", 1)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message_text,
                "sender_id": sender_id,
                "event_type": "message"
            }
        )

        if self.user and self.user.is_authenticated and sender_id == "student":
            await self.save_message(self.user.id, mentor_id, message_text)

        if sender_id == "student":
            asyncio.create_task(self.send_bot_reply(message_text, mentor_id))

    async def send_bot_reply(self, student_message, mentor_id):
        # Simulate thinking delay for realism
        await asyncio.sleep(1.5)
        
        mentors = {
            1: "Dr. Ravi Patil", 2: "Sneha Kumar", 3: "Arjun Jha",
            4: "Dr. Priya Sharma", 5: "Karthik Reddy", 6: "Ananya Gupta"
        }
        mentor_name = mentors.get(mentor_id, "Dr. Ravi Patil")
        msg = student_message.lower().strip()
        
        if not msg: return

        # --- ADVANCED INTENT MATCHING ---
        # We look for keywords and handle common typos found in the screenshot
        
        def contains_any(words):
            return any(word in msg for word in words)

        # 1. Greeting Intent
        if contains_any(["hi", "hello", "hey", "hii", "morning", "evening"]):
            replies = [
                f"Hello! I'm {mentor_name}. How can I help you with your career journey today?",
                f"Hi there! Excited to help you. What's on your mind regarding your career?",
                f"Greetings! I'm {mentor_name}. I've been looking at your profile. How can I assist?"
            ]
            reply = random.choice(replies)

        # 2. Career/Developer/Coding Intent (Screenshot Case)
        elif contains_any(["coding", "developer", "deveolper", "software", "it", "web", "full stack", "fullstack"]):
            reply = f"That's a fantastic goal! Becoming a Full Stack Developer is highly rewarding. To start, I recommend focusing on the MERN stack (MongoDB, Express, React, Node.js). Have you checked out our 'Web Development' course yet? It's perfect for getting started in IT companies."

        # 3. Resume/ATS Intent
        elif contains_any(["resume", "cv", "ats", "portfolio"]):
            reply = "Your resume is your ticket to an interview. Make sure to use clean formatting and highlight your projects. I've analyzed your current score—try adding more specific technologies you've used to boost it!"

        # 4. Job/Placement Intent
        elif contains_any(["job", "placement", "intern", "hiring", "company", "companies"]):
            reply = "Placement season is in full swing! Companies like Zoho, AWS, and Flipkart are actively looking for interns. I suggest applying to at least 3 roles today to increase your chances."

        # 5. Project/Collaboration Intent
        elif contains_any(["project", "build", "make", "create"]):
            reply = "Building projects is the best way to learn. If you're interested in web dev, try building a Task Management app or a Portfolio site. You can also find teammates in the 'Projects' tab here!"

        # 6. Study/Education/Guidance Intent
        elif contains_any(["study", "learn", "guidance", "guide", "help", "intersest"]):
            reply = "I'm here to provide all the guidance you need. We can start by identifying your core interests. Are you more drawn towards Backend logic, Frontend design, or perhaps Data Science?"

        # --- FALLBACK ---
        else:
            reply = f"I hear you! As your mentor, I'd suggest we break this down into smaller steps. Could you tell me more about your current skills or what you've enjoyed studying so far?"

        # Final Broadcast
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": reply,
                "sender_id": "mentor",
                "event_type": "message"
            }
        )

        if self.user and self.user.is_authenticated:
            await self.save_message(mentor_id, self.user.id, reply)

    @database_sync_to_async
    def save_message(self, sender_id, receiver_id, text):
        from mentorship.models import Message
        User = get_user_model()
        try:
            sender = User.objects.get(id=sender_id)
            receiver = User.objects.get(id=receiver_id)
            Message.objects.create(sender=sender, receiver=receiver, text=text)
        except User.DoesNotExist:
            pass

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender_id": event["sender_id"],
            "event_type": event["event_type"]
        }))