from django.db import models
from whizzo_app.models import BaseModel


class FeaturesModel(BaseModel):
    name= models.CharField(max_length=255)
    class Meta:
        db_table = "Features"