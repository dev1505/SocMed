import os

import ChatApp.urls  # where websocket_urlpatterns is
import django
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SocialMedia.settings")
django.setup()

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),  # DRF/HTTP requests
        "websocket": AuthMiddlewareStack(URLRouter(ChatApp.urls.websocket_urlpatterns)),
    }
)
