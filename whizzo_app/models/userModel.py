from django.db import models
from django.contrib.auth.models import AbstractUser
from whizzo_app.models.uploadMediaModel import UploadMediaModel
from whizzo_app.utils.choiceFields import PROFILE_STATUS_OPTIONS

class UserModel(AbstractUser):

    profile_picture = models.ForeignKey(UploadMediaModel, on_delete=models.SET_NULL, null=True)

    phone_no = models.CharField(max_length=100, default="")
    otp = models.CharField(max_length=100, default="")

    profile_status = models.IntegerField(choices=PROFILE_STATUS_OPTIONS, default=0)

    otp_sent_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "User"