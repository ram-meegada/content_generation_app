from django.db import models
from whizzo_app.models import BaseModel, UploadMediaModel



class TestimonialModel(BaseModel):
    profile_picture = models.ForeignKey(UploadMediaModel, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=255, default="")
    last_name = models.CharField(max_length=255, default="")
    country_code = models.CharField(max_length=10,default="")
    email = models.CharField(max_length=255, default="")
    phone_no = models.CharField(max_length=100, default="")
    rating = models.FloatField(default=0)
    message = models.CharField(max_length=255, default="")

    class Meta:
        db_table = "Testimonial"