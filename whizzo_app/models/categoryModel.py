from django.db import models
from whizzo_app.models.baseModel import BaseModel
from whizzo_app.models.userModel import UserModel
from whizzo_app.models.uploadMediaModel import UploadMediaModel
from whizzo_app.utils.choiceFields import CATEGORY_CHOICES, SUB_CATEGORY_CHOICES

class CategoryModel(BaseModel):

    #foreinkey fields
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    media = models.ForeignKey(UploadMediaModel, on_delete=models.CASCADE, null=True)

    #integer fields
    category = models.IntegerField(choices=CATEGORY_CHOICES, default=0)
    sub_category = models.IntegerField(choices=SUB_CATEGORY_CHOICES, default=0)
    correct_answers = models.IntegerField(blank=True, null=True)

    topic = models.TextField(default="")
    page = models.IntegerField(default=0)
    tone = models.TextField(default="")
    reference = models.TextField(default="")
    research_file_links = models.JSONField(default=list)
    reduced_citations = models.BooleanField(default=False)
    description = models.TextField(default="")
    research_type = models.IntegerField(default=1)
    #others
    result = models.JSONField(default=list)
    download_file = models.TextField(default="")
    download_doc_file = models.TextField(default="")

    class Meta:
        db_table = "Category"