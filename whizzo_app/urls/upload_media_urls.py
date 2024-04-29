from django.urls import path
from whizzo_app.views import uploadMediaView

urlpatterns = [
    path("upload/", uploadMediaView.UploadMediaView.as_view())
]