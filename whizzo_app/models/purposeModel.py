from django.db import models
from whizzo_app.models import BaseModel



class PurposeModel(BaseModel):
    name= models.CharField(max_length=255)
    detail = models.CharField(max_length=255)

    class Meta:
        db_table = "Purpose"