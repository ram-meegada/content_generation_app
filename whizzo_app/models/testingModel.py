from whizzo_app.models.baseModel import BaseModel
from whizzo_app.models import UserModel
from whizzo_app.utils.choiceFields import SUB_CATEGORY_CHOICES
from django.db import models

class TestingModel(BaseModel):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    sub_category = models.IntegerField(choices=SUB_CATEGORY_CHOICES, default=1)
    sub_category_type = models.IntegerField(default=1)

    result = models.JSONField(default=list)
    correct_answers = models.IntegerField(default=0)
    wrong_answers = models.IntegerField(default=0)
    remaining_answers = models.IntegerField(default=0)

    class Meta:
        db_table = "testing_table"
