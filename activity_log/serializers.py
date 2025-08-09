from rest_framework import serializers
from .models import ActivityLog

class ActivityLogSerializer(serializers.ModelSerializer):
    """
    Serializer for the ActivityLog model.

    This serializer is used to represent ActivityLog instance and serialize and
    deserialize the fields of ActivityLog model.

    fields : __all__
    read_only_fields: []
    """
    class Meta:
        model = ActivityLog
        fields = '__all__'