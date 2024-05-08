from django.db import models
from whizzo_app.models import BaseModel

class FaqModel(BaseModel):
    question = models.TextField()
    answer = models.TextField()
    

    class Meta:
        db_table = "Faq"