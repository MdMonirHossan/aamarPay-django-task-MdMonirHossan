from django.urls import path
from .views import (
    InitiatePaymentView,
    FileUploadView,
    FileListView, 
    TransactionListView,
    payment_success,
    payment_cancel,
    payment_failed
)

urlpatterns = [
    # DRF API urls
    path('initiate-payment', InitiatePaymentView.as_view(), name='payment_initiate'),
    path('upload', FileUploadView.as_view(), name='upload_file'),
    path('files', FileListView.as_view(), name='file_list'),
    path('transactions', TransactionListView.as_view(), name='transaction_list'),

    # Aamarpay callback urls
    path('success', payment_success, name='success_page'),
    path('cancel', payment_cancel, name='cancel_page'),
    path('failed', payment_failed, name='failed_page'),
]