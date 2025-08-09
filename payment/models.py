from django.db import models
from libs.core.models.base_models import BaseModel
from django.contrib.auth.models import User
from libs.utils.constants.model_constants import FILE_STATUS_CHOICES

# Create your models here.
class FileUpload(BaseModel):
    """
    This model/entity is responsible for storing all data for file uploads.
    inheritance: BaseModel
    relations: [User]
    ordering: [-create_at]
    """
    user        = models.ForeignKey(User, related_name='uploads', on_delete=models.CASCADE,)
    file        = models.FileField(upload_to='uploads/')
    filename    = models.CharField(max_length=255)
    status      = models.CharField(max_length=20, choices=FILE_STATUS_CHOICES, default='processing')
    word_count  = models.PositiveBigIntegerField(null=True, blank=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.filename} {self.status}'
    

class PaymentTransaction(BaseModel):
    """
    This models/entity is responsible for storing all data for user transactions
    inheritance: BaseModel
    relations: [User]
    ordering: [-created_at] 
    """
    user             = models.ForeignKey(User, related_name='transactions', on_delete=models.CASCADE)
    transaction_id   = models.CharField(max_length=255)
    amount           = models.DecimalField(max_digits=10, decimal_places=2)
    status           = models.CharField(max_length=50)
    gateway_response = models.JSONField()

    class Meta:
        verbose_name_plural = 'Transactions'
        ordering            = ('-created_at',)

    def __str__(self):
        return self.transaction_id

    

