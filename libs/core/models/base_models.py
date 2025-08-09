from django.db import models

class BaseModel(models.Model):
    """
    @model: BaseModel
    @inheritance: models.Model
    @is_abstract: True
    @description: this base is an abstract model for all other models.
    """
    created_at = models.DateTimeField(auto_now_add=True, help_text='Date time when a entry is created.')
    updated_at = models.DateTimeField(auto_now=True, help_text='Date time when a entry is updated.')

    class Meta:
        abstract = True