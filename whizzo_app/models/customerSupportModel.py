from django.db import models
from whizzo_app.models.userModel import UserModel
from whizzo_app.models.baseModel import BaseModel

class CustomerSupportModel(BaseModel):
    customer = models.ForeignKey(UserModel, on_delete=models.CASCADE, blank=True, null=True)
    username = models.CharField(max_length=255)
    queries = models.TextField()
    email = models.CharField(default="")
    answer = models.TextField(blank=True, null=True)
    reverted_back = models.BooleanField(default=False)

    class Meta:
        db_table = "CustomerSupport"