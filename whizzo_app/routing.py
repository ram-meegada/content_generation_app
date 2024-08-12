from django.urls import path
from whizzo_app.consumers import *

websocket_urlpatterns = [
    path('file-summarization/', FileSummarizationConsumer.as_asgi()),

]
