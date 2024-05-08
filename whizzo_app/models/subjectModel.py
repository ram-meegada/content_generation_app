from django.db import models


class SubjectModel(models.Model):
    subject_name = models.CharField(max_length=255, default="")
    subject_detail = models.CharField(max_length=255, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "Subject"