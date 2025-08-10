import requests, json
from django.shortcuts import render
from django.utils import timezone
from rest_framework import views, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from decouple import config
from .models import FileUpload, PaymentTransaction
from .serializers import (
    FileUploadSerializer, 
    PaymentTransactionSerializer,
    PaymentInitiateSerializer,
)

# Create your views here.

class InitiatePaymentView(views.APIView):
    """
    
    """
    permission_classes  = [IsAuthenticated]
    def post(self, request):
        print('data ----- ', request.data)
        serializer = PaymentInitiateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        req_data = serializer.validated_data
        print('------------ reqe data ', req_data)
        payment_url = config('PAYMENT_URL')
        payload = {
            "store_id": config('STORE_ID'),
            "signature_key": config('SIGNATURE_KEY'),
            "success_url": request.build_absolute_uri(config('SUCCESS_URL')),
            "fail_url": request.build_absolute_uri(config('FAIL_URL')),
            "cancel_url": request.build_absolute_uri(config('CANCEL_URL')),
            "tran_id": f"trn{timezone.now().timestamp()}",
            "amount": str(req_data['amount']),
            "currency": req_data['currency'],
            "desc": req_data['description'],
            "cus_name": request.user.username,
            "cus_email": request.user.email,
            "cus_add1": req_data['customer_add1'],
            "cus_add2": req_data['customer_add1'],
            "cus_city": req_data['customer_city'],
            "cus_state": req_data['customer_state'],
            "cus_postcode": req_data['customer_postcode'],
            "cus_country": req_data['customer_country'],
            "cus_phone": req_data['customer_phone'],
            "type": "json"
        }
        headers = {
            'Content-Type': 'application/json'
        }
        print('----- payload ', payload)
        response = requests.post(
            payment_url, 
            json=payload,
            headers=headers
        )
        print('----- response --- ', response)
        try:
            data = response.json()
            if bool(data.get('result')):
                return Response({"payment_url": data.get('payment_url')})
            return Response({'error': 'Payment initiation failed'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'Payment initiation failed'}, status=500)


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
    

def payment_success(request):
    context = {}
    return render(request, 'payment_success.html', context)

def payment_cancel(request):
    context = {}
    return render(request, 'payment_cancel.html', context)

def payment_failed(request):
    context = {}
    return render(request, 'payment_failed.html', context)