from django.db import models
from whizzo_app.models.baseModel import BaseModel
from whizzo_app.models.userModel import UserModel
from whizzo_app.models.uploadMediaModel import UploadMediaModel

class ArticleModel(BaseModel):

    #foreinkey fields
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    topic = models.TextField(default="")
    language = models.CharField(max_length=100, default="")
    region = models.CharField(max_length=100, default="")
    pov = models.CharField(max_length=100, default="")
    words = models.IntegerField(default=0)
    tone = models.CharField(max_length=100, default="")
    file_name = models.CharField(max_length=100, blank=True, null=True)

    all_topics = models.JSONField(default=list)

    #others
    result = models.JSONField(default=list)
    download_file = models.TextField(default="")
    download_doc_file = models.TextField(default="")

    class Meta:
        db_table = "Article"