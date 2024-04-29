from whizzo_app.models import BaseModel
from django.db import models

class UploadMediaModel(BaseModel):
    media_url = models.CharField(max_length=255, default="")
    media_type = models.CharField(max_length=255, default="")
    media_name = models.CharField(max_length=255, default="")
    media_size = models.CharField(max_length=255, default="")

    class Meta:
        db_table = "Media"