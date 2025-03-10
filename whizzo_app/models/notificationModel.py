from whizzo_app.models.baseModel import BaseModel
from django.db import models
from whizzo_app.models import UserModel

NOTIFICATION_TYPE = [(1, "push notification"), (2, "email")]
NOTIFICATION_FOR = [(1, "all"), (2, "user"), (3, "subadmin")]

class NotificationModel(BaseModel):
    title = models.CharField(max_length=1000, null=True, blank=True)  
    message = models.TextField(null=True, blank=True)
    notification_type = models.IntegerField(choices = NOTIFICATION_TYPE, default=1)  
    notification_for = models.IntegerField(default=1)
    # is_arabic = models.BooleanField(default=False)
    title_ar = models.CharField(max_length=100, null=True, blank=True)
    message_ar = models.TextField(null=True, blank=True)
 
    def __unicode__(self):
        return self.id
    
    class Meta:
        db_table = 'Notification_Detail'