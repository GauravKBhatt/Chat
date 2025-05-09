from django.urls import path
from .import consumers

websocket_urlpatterns=[
    path('ws/<str:room_name>/',consumers.ChatConsumer.as_asgi()),
    # i want to create another consumer too to learn. path('ws/')
]