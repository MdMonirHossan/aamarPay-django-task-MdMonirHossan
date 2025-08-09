from rest_framework import views, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import FileUpload, PaymentTransaction
from .serializers import FileUploadSerializer, PaymentTransactionSerializer


# Create your views here.
class FileListView(generics.ListAPIView):
    """
    This List API view is responsible for providing a list of uploaded files by requested user.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = FileUploadSerializer

    def get_queryset(self):
        '''
        Return a queryset of files only for the requested user.
        '''
        return FileUpload.objects.filter(user=self.request.user)

class TransactionListView(generics.ListAPIView):
    """
    This List API view is responsible for providing a list of transactions by requested user.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentTransactionSerializer

    def get_queryset(self):
        '''
        Return a queryset of transactions only for the requested user.
        '''
        return PaymentTransaction.objects.filter(user=self.request.user)