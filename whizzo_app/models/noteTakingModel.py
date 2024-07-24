from django.db import models
from whizzo_app.models.baseModel import BaseModel
from whizzo_app.models.userModel import UserModel

class NoteTakingModel(BaseModel):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, blank=True, null=True)
    type = models.IntegerField(default=1)
    binary_data = models.TextField(blank=True)
    note_screenshot = models.TextField(default="")
    canvas_height = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = "Note Taking"
