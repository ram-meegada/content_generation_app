from django.db import models
from whizzo_app.models.baseModel import BaseModel
from whizzo_app.models.userModel import UserModel
from whizzo_app.models.uploadMediaModel import UploadMediaModel
from whizzo_app.utils.choiceFields import  SUB_CATEGORY_CHOICES

class FileSumarizationModel(BaseModel):

    #foreinkey fields
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    media = models.ForeignKey(UploadMediaModel, on_delete=models.CASCADE, null=True)

    #integer fields
    sub_category = models.IntegerField(choices=SUB_CATEGORY_CHOICES, default=0)
    # correct_answers = models.IntegerField(blank=True, null=True)
    download_file = models.TextField(default="")
    download_highlighted_file = models.TextField(default="")

    #others
    result = models.JSONField(default=list)

    class Meta:
        db_table = "FileSumarization"