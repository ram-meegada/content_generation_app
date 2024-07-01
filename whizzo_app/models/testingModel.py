from whizzo_app.models.baseModel import BaseModel
from whizzo_app.models import UserModel
from django.db import models

class TestingModel(BaseModel):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    result = models.JSONField(default=list)
    correct_answers = models.IntegerField(default=0)
    wrong_answers = models.IntegerField(default=0)
    remaining_answers = models.IntegerField(default=0)

    class Meta:
        db_table = "testing_table"
