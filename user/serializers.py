from django.contrib.auth.models import User
from rest_framework import serializers

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    This serializer class is responsible for serializing and deserializing data
    fields for user model

    Returns:
        obj - User object
    """
    email      = serializers.EmailField()
    password   = serializers.CharField(write_only=True, min_length=6)


    class Meta:
        model   = User
        fields  = ['username', 'email', 'password']


    def create(self, validate_data):
        '''
        Create a new user by serializer fields.
        '''
        user = User.objects.create_user(
            username  = validate_data.get('username'),
            email     = validate_data.get('email'),
            password  = validate_data.get('password'),
        )
        return user