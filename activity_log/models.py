from django.db import models
from django.contrib.auth.models import User
from libs.core.models.base_models import BaseModel

# Create your models here.
class ActivityLog(BaseModel):
    """
    This model/entity is responsible to store various user activity logs within the application.
    """
    user        = models.ForeignKey(
                    User, 
                    related_name='activities', 
                    on_delete=models.CASCADE, 
                    help_text='The user who performed the action'
                )
    action      = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    metadata    = models.JSONField()

    class Meta:
        verbose_name_plural = 'Activity Logs'
        ordering = ('-created_at',)

    def __str__(self):
        return f"{self.user.username} | {self.action} | {self.created_at.strftime('%Y-%m-%d %H:%M:%s')}"