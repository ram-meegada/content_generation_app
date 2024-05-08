from django.db import models
from whizzo_app.models import BaseModel, UserModel, RatingModel



class TestimonialModel(BaseModel):
    rating = models.ForeignKey(RatingModel,on_delete=models.CASCADE, null=True)
    message = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(UserModel,on_delete=models.CASCADE, null=True)


    class Meta:
        db_table = "Testimonial"