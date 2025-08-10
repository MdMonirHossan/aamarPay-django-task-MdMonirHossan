import requests, json
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework import views, generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from decouple import config
from libs.utils.constants.model_constants import PAYMENT_STATUS_CHOICES
from activity_log.models import ActivityLog
from .models import FileUpload, PaymentTransaction
from .serializers import (
    FileUploadSerializer, 
    PaymentTransactionSerializer,
    PaymentInitiateSerializer,
)
from .utils import update_transaction
from .celery_task import process_file_word_count

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
                # Create user activity
                ActivityLog.objects.create(
                    user=request.user, 
                    action="Payment Initiate", 
                    description = f"Payment initiated by {request.user} and transaction id {transaction_id}",
                    metadata=data
                )
                return Response({"payment_url": data.get('payment_url')})
            return Response({'error': 'Payment initiation failed'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=500)


# class FileUploadView(generics.CreateAPIView):
#     """
#     Allows file uploads only if user has a complete a successful payment.
#     if the payment is successful then can_upload_file flag is change to True

#     Returns:
#         Obj: FileUpload
#     """
#     serializer_class = FileUploadSerializer
#     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         '''
        
#         '''
#         # Check for payment eligibility
#         latest_payment = PaymentTransaction.objects.filter(
#             user = self.request.user,
#             can_upload_file = True,
#             status = 'success'
#         ).order_by('-completed_at').first()

#         # Return response if latest payment not found
#         if not latest_payment:
#             return Response({"error": "You must complete a payment before uploading file."}, status=status.HTTP_400_BAD_REQUEST)
        
#         # data sanitization from serializer
#         data = serializer.validated_data
#         file = self.request.FILES.get('file')
#         if 'filename' not in data or data['filename'] == "":
#             filename = file.name.split('.')[0]
#         else:
#             filename = data['filename']

#         # save upload file data
#         upload_file = serializer.save(
#             user = self.request.user, 
#             filename = filename,
#             upload_time = timezone.now()
#         )

#         # Make payment as used
#         latest_payment.can_upload_file = False
#         latest_payment.save()

#         # Create activity log for file upload
#         metadata = {
#             "status" : upload_file.status,
#             "upload_time" : str(upload_file.upload_time),
#             "filename" : file.name,
#             "file_size": file.size,
#             "content_type": file.content_type,
#         }
#         # Create activity log for file upload
#         ActivityLog.objects.create(
#             user = self.request.user,
#             action = 'File Upload',
#             description = f"File {filename} uploaded after successful payment.",
#             metadata = metadata
#         )
#         return Response(upload_file, status=status.HTTP_201_CREATED)

class FileUploadView(views.APIView):
    """
    Allows file uploads only if user has a complete a successful payment.
    if the payment is successful then can_upload_file flag is change to True

    Returns:
        Obj: FileUpload
    """
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        # Check for payment eligibility
        latest_payment = PaymentTransaction.objects.filter(
            user = self.request.user,
            can_upload_file = True,
            status = 'success'
        ).order_by('-completed_at').first()

        # Return response if latest payment not found
        if not latest_payment:
            return Response(
                {"error": "You must complete a payment before uploading file."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get file
        file = request.FILES.get('file')
        if not file:
            return Response(
                {"error": "No file provided"},
                status = status.HTTP_400_BAD_REQUEST
            )
        
        # Validate file extension
        extension = file.name.split('.')[-1].lower()
        if extension not in ['txt', 'docx']:
            return Response(
                {"error": f'Invalid file type. Allowed only .txt & .docs file.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # File name
        filename = request.data.get('filename') or file.name.split('.')[0]

        # validate and save file record via serializer
        serializer = FileUploadSerializer(data={
            "file": file,
            "filename": filename
        })
        serializer.is_valid(raise_exception=True)
        upload_file = serializer.save(user=request.user, upload_time=timezone.now())

        # Make payment as used
        latest_payment.can_upload_file = False
        latest_payment.save()

        # Create activity log for file upload
        metadata = {
            "status" : upload_file.status,
            "upload_time" : str(upload_file.upload_time),
            "filename" : file.name,
            "file_size": file.size,
            "content_type": file.content_type,
        }

        # Create activity log for file upload
        ActivityLog.objects.create(
            user = self.request.user,
            action = 'File Upload',
            description = f"File {filename} uploaded after successful payment.",
            metadata = metadata
        )

        # Trigger celery task for word count
        process_file_word_count.delay(upload_file.id)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        

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
        if data['pay_status'] == 'Successful':
            
            # Utility function for updating transaction
            update_transaction(data, 'success', True)

            # Create user activity
            try:
                user = User.objects.get(username=data['cus_name'])
                ActivityLog.objects.create(
                    user = user, 
                    action = "Payment Successful", 
                    description = f"Payment successful and transaction id {data['mer_txnid']}",
                    metadata = data
                )
            except:
                pass
        return render(request, 'payment_success.html', context)
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def payment_cancel(request):
    context = {}
    return render(request, 'payment_cancel.html', context)

@csrf_exempt
def payment_failed(request):
    context = {}
    if request.method == "POST":
        data = request.POST.dict()  # form data sent by aamarPay
        if data['pay_status'] == 'Failed':
            
            # Utility function for updating transaction
            update_transaction(data, 'failed')

            # Create user activity
            try:
                user = User.objects.get(username=data['cus_name'])
                ActivityLog.objects.create(
                    user = user, 
                    action = "Payment Failed", 
                    description = f"Payment failed and transaction id {data['mer_txnid']}",
                    metadata = data
                )
            except:
                pass
        return render(request, 'payment_failed.html', context)
    return JsonResponse({"error": "Invalid request"}, status=400)