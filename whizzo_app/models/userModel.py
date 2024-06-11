from django.db import models
from django.contrib.auth.models import AbstractUser
from whizzo_app.models import BaseModel
from whizzo_app.models.subRoleModel import SubRoleModel
from whizzo_app.models.uploadMediaModel import UploadMediaModel
from whizzo_app.models.purposeModel import PurposeModel
from whizzo_app.utils.choiceFields import PROFILE_STATUS_OPTIONS,USER_ROLE_CHOICES





class UserModel(AbstractUser, BaseModel):

    profile_picture = models.ForeignKey(UploadMediaModel, on_delete=models.SET_NULL, null=True)
    purpose = models.ForeignKey(PurposeModel, on_delete=models.SET_NULL, null=True)
    username= models.CharField(max_length=255, blank=True, null=True, unique=True)
    name = models.CharField(max_length=255, default="")
    phone_no = models.CharField(max_length=100, default="")
    country_code = models.CharField(max_length=17, default="")
    country_name = models.CharField(max_length=17, default="")
    otp = models.CharField(max_length=100, default="")

    profile_status = models.IntegerField(choices=PROFILE_STATUS_OPTIONS, default=0)
    email_verification = models.BooleanField(default=False)
    phone_verification = models.BooleanField(default=False)
    otp_sent_time = models.DateTimeField(blank=True, null=True)
    role = models.IntegerField(choices = USER_ROLE_CHOICES, default=0) 
    sub_role = models.ForeignKey(SubRoleModel, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = "User"