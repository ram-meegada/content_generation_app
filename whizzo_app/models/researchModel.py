from django.db import models
from whizzo_app.models.baseModel import BaseModel
from whizzo_app.models.userModel import UserModel
from whizzo_app.models.uploadMediaModel import UploadMediaModel
from whizzo_app.utils.choiceFields import  SUB_CATEGORY_CHOICES, TONE_OF_VOICE, SPECIFY_REFERENCE

class ReseaerchModel(BaseModel):

    #foreinkey fields
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    topic= models.CharField(max_length=255, blank=True, null=True)
    page= models.CharField(max_length=255, blank=True, null=True)
    tone_of_voice= models.CharField(max_length=255, blank=True, null=True)
    specify_reference= models.CharField(max_length=255, blank=True, null=True)
    is_reduce_citation = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    media = models.ForeignKey(UploadMediaModel, on_delete=models.CASCADE, null=True)
    #integer fields
    sub_category = models.IntegerField(choices=SUB_CATEGORY_CHOICES, default=0)
    # correct_answers = models.IntegerField(blank=True, null=True)

    #others
    result = models.JSONField(default=list)

    class Meta:
        db_table = "Research"