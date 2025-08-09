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
        read_only_fields = ['status', 'word_count', 'crated_at']