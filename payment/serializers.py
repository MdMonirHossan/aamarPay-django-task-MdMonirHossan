import os
from decimal import Decimal
from rest_framework import serializers
from .models import PaymentTransaction, FileUpload


class PaymentTransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for the PaymentTransaction model.

    This serializer is used to represent PaymentTransaction instance and serialize and
    deserialize the fields of PaymentTransaction model.

    fields : __all__
    read_only_fields: []
    """
    class Meta:
        model = PaymentTransaction
        fields = '__all__'

class FileUploadSerializer(serializers.ModelSerializer):
    """
    Serializer for the FileUpload model.

    This serializer is used to represent FileUpload instance and serialize and
    deserialize the fields of FileUpload model.

    fields : __all__
    read_only_fields: ['status', 'word_count', 'crated_at']
    """
    class Meta:
        model = FileUpload
        fields = '__all__'
        read_only_fields = ['user', 'status', 'word_count', 'crated_at']

class PaymentInitiateSerializer(serializers.Serializer):
    """
    Serializer for Initiating payment.

    This serializer is used to represent FileUpload instance and serialize and
    deserialize the fields of FileUpload model.
    """
    amount              = serializers.DecimalField(
                            max_digits=10, 
                            decimal_places=2, 
                            default=100.0,
                            min_value=Decimal('100.0')   # User must have to pay 100
                        )
    currency            = serializers.CharField(max_length=10, required=False, default='BDT')
    description         = serializers.CharField(max_length=255)
    customer_add1       = serializers.CharField(max_length=255, required=False)
    customer_add2       = serializers.CharField(max_length=255, required=False)
    customer_city       = serializers.CharField(max_length=100, default='Dhaka', required=False)
    customer_state      = serializers.CharField(max_length=100, default='Dhaka', required=False)
    customer_postcode   = serializers.CharField(max_length=100, default='1234', required=False)
    customer_country    = serializers.CharField(max_length=100, default='Bangladesh', required=False)
    customer_phone      = serializers.CharField(max_length=50)

