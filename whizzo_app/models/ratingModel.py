from django.db import models
from whizzo_app.models import BaseModel, UserModel



class RatingModel(BaseModel):
    ratings = models.FloatField(default=0)
    description = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(UserModel,on_delete=models.CASCADE, null=True)


    class Meta:
        db_table = "Rating"