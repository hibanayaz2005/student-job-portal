"""
ASGI config for careerbridge project.
Handles both HTTP and WebSocket connections via Django Channels.
"""

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "careerbridge.settings")

django.setup()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from django.core.management import call_command
from dashboard.routing import websocket_urlpatterns

import time
import sys

max_retries = 5
for i in range(max_retries):
    try:
        call_command('migrate', interactive=False)
        print("Migrations applied successfully!")
        break
    except Exception as e:
        print(f"Migration failed during ASGI startup (attempt {i+1}/{max_retries}): {e}")
        if "database is locked" in str(e).lower() or "operationalerror" in str(e).lower():
            time.sleep(2)
        else:
            break

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})