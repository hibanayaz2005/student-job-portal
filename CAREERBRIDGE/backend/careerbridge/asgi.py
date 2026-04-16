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
from dashboard.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})