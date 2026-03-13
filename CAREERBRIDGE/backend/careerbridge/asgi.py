
import os
import django

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from dashboard.routing import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "careerbridge.settings")

django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),

    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})

"""
ASGI config for careerbridge project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'careerbridge.settings')

application = get_asgi_application()

from dotenv import load_dotenv
import os

load_dotenv()

FAST2SMS_API_KEY = os.getenv("FAST2SMS_API_KEY")