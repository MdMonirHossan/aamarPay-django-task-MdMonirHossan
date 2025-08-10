import requests, json
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from rest_framework import views, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from decouple import config
from libs.utils.constants.model_constants import PAYMENT_STATUS_CHOICES
from .models import FileUpload, PaymentTransaction
from .serializers import (
    FileUploadSerializer, 
    PaymentTransactionSerializer,
    PaymentInitiateSerializer,
)

# Create your views here.

class InitiatePaymentView(views.APIView):
    """
    This API view is handling initiate a payment to aamarpay sandbox payment gateway.
    After successful request it will return a payment url.

    Permissions:
        IsAuthenticated
    
    Serializer:
        PaymentInitiateSerializer

    Returns:
        Response with payment_url or error.
    """
    permission_classes  = [IsAuthenticated]
    def post(self, request):
        serializer = PaymentInitiateSerializer(data=request.data)
        # raise exception for invalid data
        serializer.is_valid(raise_exception=True)
        req_data = serializer.validated_data
        # sandbox url for env
        payment_url = config('PAYMENT_URL')
        # initiate payment request payload
        transaction_id = f"trn{timezone.now().timestamp()}"
        payload = {
            "store_id": config('STORE_ID'),
            "signature_key": config('SIGNATURE_KEY'),
            "success_url": request.build_absolute_uri(config('SUCCESS_URL')),
            "fail_url": request.build_absolute_uri(config('FAIL_URL')),
            "cancel_url": request.build_absolute_uri(config('CANCEL_URL')),
            "tran_id": transaction_id,
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
        # Request to the aamarpay sandbox
        response = requests.post(
            payment_url, 
            json=payload,
            headers=headers
        )
        # handling response
        try:
            data = response.json()
            if bool(data.get('result')):
                # Create pending transaction
                PaymentTransaction.objects.create(
                    user=request.user,
                    transaction_id=transaction_id,
                    amount=req_data['amount'],
                    status='pending'
                )
                return Response({"payment_url": data.get('payment_url')})
            return Response({'error': 'Payment initiation failed'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=500)


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
    
@csrf_exempt
def payment_success(request):
    """
    Handles the payment success callback from AamarPay
    """
    context = {}
    if request.method == "POST":
        data = request.POST.dict()  # form data sent by aamarPay
        print("✅ Payment success POST data:", data)
        if data['pay_status'] == 'Successful':
            transaction_id = data['mer_txnid']

            # Get PaymentTransaction instance by transaction id
            transaction = get_object_or_404(PaymentTransaction, transaction_id=transaction_id)
            # Update transaction and enable file upload status for user
            transaction.status           = 'success'
            transaction.can_upload_file  = True
            transaction.complete_at      = timezone.now()
            transaction.gateway_response = data
            transaction.save()
        return render(request, 'payment_success.html', context)
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def payment_cancel(request):
    context = {}
    return render(request, 'payment_cancel.html', context)

@csrf_exempt
def payment_failed(request):
    context = {}
    return render(request, 'payment_failed.html', context)