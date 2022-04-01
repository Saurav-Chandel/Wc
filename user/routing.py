from django.urls import path
from user import consumers
from django.urls import re_path

websocket_urlpattrens=[
    path('ws/sc/',consumers.MySyncConsumer.as_asgi()),
    path('ws/ac/',consumers.MyAsyncConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]