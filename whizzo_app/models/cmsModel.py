from django.db import models
from whizzo_app.models import BaseModel



class CmsModel(BaseModel):
    about_us = models.TextField( blank=True, null=True)
    terms_condition = models.TextField( blank=True, null=True)
    privacy_policy = models.TextField( blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    phone_no = models.CharField(max_length=20, blank=True, null=True)
    country_code = models.CharField(max_length=17, default="")

    class Meta:
        db_table = "CMS"