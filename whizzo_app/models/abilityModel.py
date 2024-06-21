from django.db import models
from django.contrib.postgres.fields import ArrayField

class AbilityModel(models.Model):
    question = models.CharField(max_length=255, default="")
    answer_option=ArrayField(models.CharField(max_length=255,default=""), blank=True, null=True)
    corect_answer = models.CharField(max_length=255, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    is_mcq = models.BooleanField(default=False)
    is_arabic = models.BooleanField(default=False)

    class Meta:
        db_table = "Ability"