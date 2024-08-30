from django.db import models
from whizzo_app.models.baseModel import BaseModel
from whizzo_app.models.userModel import UserModel
from whizzo_app.models.uploadMediaModel import UploadMediaModel

class AssignmentModel(BaseModel):

    #foreinkey fields
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    media = models.ForeignKey(UploadMediaModel, on_delete=models.CASCADE, null=True , related_name="pdf_file")
    binary_data = models.JSONField(default="")
    #others
    language = models.CharField(default="English")
    result = models.JSONField(default=list)
    download_file = models.TextField(default="")
    download_doc_file = models.TextField(default="")
    file_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = "Assignment"