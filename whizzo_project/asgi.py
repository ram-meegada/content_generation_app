import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import whizzo_app.routing
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'whizzo_project.settings')

wsgi_application = get_asgi_application()
application = ProtocolTypeRouter(
    {
        "http": wsgi_application,
        "websocket": AuthMiddlewareStack
        (
            URLRouter(
                whizzo_app.routing.websocket_urlpatterns
            )
        )
    }
)
