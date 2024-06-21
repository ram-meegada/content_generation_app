from django.db import models
from whizzo_app.models import BaseModel



class PurposeModel(BaseModel):
    name= models.CharField(max_length=255)
    detail = models.CharField(max_length=255)
    # is_arabic = models.BooleanField(default=False)
    name_ar = models.CharField(max_length=255,default="")
    detail_ar = models.CharField(max_length=255,default="")

    class Meta:
        db_table = "Purpose"