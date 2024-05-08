from django.db import models
from whizzo_app.models import UserModel
from whizzo_app.models.moduleModel import ModuleModel
class PermissionModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    module = models.ForeignKey(ModuleModel, on_delete=models.CASCADE, null=True)

    can_add_edit = models.BooleanField(default=False)
    can_view = models.BooleanField(default=False)
    can_be_delete = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=True)


    class Meta:
        db_table = 'Permissions' 
