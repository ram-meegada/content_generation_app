from django.db import models
from whizzo_app.models import BaseModel
from whizzo_app.utils.choiceFields import PLAN_CHOICES
from whizzo_app.models.featureModel import FeaturesModel

class SubscriptionModel(BaseModel):
    price = models.CharField(max_length=255)
    features = models.ManyToManyField(FeaturesModel)
    plan_type = models.IntegerField(choices=PLAN_CHOICES, blank=True, null=True)
    class Meta:
        db_table = "Subscription" 