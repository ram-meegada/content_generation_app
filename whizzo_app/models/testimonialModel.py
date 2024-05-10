from django.db import models
from whizzo_app.models import BaseModel



class TestimonialModel(BaseModel):
    first_name = models.CharField(max_length=255, default="")
    last_name = models.CharField(max_length=255, default="")
    email = models.CharField(max_length=255, default="")
    phone_no = models.CharField(max_length=100, default="")
    rating = models.FloatField(default=0)
    message = models.CharField(max_length=255, default="")

    class Meta:
        db_table = "Testimonial"