from django.urls import path
from .consumer import ChatConsumer

ws_urlpatterns = [
    path('ws/chat/', ChatConsumer.as_asgi())
]
