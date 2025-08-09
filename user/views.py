from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import UserRegistrationSerializer

# Create your views here.

class UserRegistrationView(generics.CreateAPIView):
    """
    Register a new user with minimal user model fields.
    serializers: UserRegistrationSerializer
    permissions: [AllowAny]
    """
    serializer_class    = UserRegistrationSerializer
    permission_classes  = (AllowAny,)

    def create(self, request, *args, **kwargs):
        '''
        override default create method for creating a new user.
        '''
        return super().create(request, *args, **kwargs)
