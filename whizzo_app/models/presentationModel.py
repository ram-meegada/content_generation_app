from django.db import models
from whizzo_app.models.baseModel import BaseModel
from whizzo_app.models.userModel import UserModel

class PresentationModel(BaseModel):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, blank=True, null=True)
    template_id = models.IntegerField(blank=True, null=True)
    slides = models.IntegerField(default=6)
    text = models.TextField(blank=True)
    binary_data = models.TextField(blank=True)
    is_arabic = models.BooleanField(default=False)

    class Meta:
        db_table = "Presentation"
