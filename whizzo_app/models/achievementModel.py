from django.db import models
from django.contrib.postgres.fields import ArrayField
from whizzo_app.models.subjectModel import SubjectModel



class AchievementModel(models.Model):
    question = models.CharField(max_length=255, default="")
    subject=models.ForeignKey(SubjectModel, on_delete=models.CASCADE,default="")
    answer_option=ArrayField(models.CharField(max_length=255,default=""), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "Acheivement"