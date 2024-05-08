from django.db import models
from whizzo_app.models.baseModel import BaseModel

class ModuleModel(BaseModel):
    module_name = models.CharField(max_length=255, default="")

    class Meta:
        db_table = "Module"