from django.urls import path
from whizzo_app.consumers import *

websocket_urlpatterns = [
    path('file-summarization/', FileSummarizationConsumer.as_asgi()),
    path('testing/generate-response/', TestingConsumer.as_asgi()),
    path('assignment-solutions/', AssignmentSolutionsConsumer.as_asgi()),
    path('generate-article/', ArticleConsumer.as_asgi()),
    path('audio-to-text/', AudioConsumer.as_asgi()),
    path('research-topics/', ResearchTopicsConsumer.as_asgi()),
    path('detailed-research/', DetailedResearchConsumer.as_asgi()), 
    path('research-topics-based-on-reference/', ResearchTopicsByReferenceConsumer.as_asgi()), 
]
