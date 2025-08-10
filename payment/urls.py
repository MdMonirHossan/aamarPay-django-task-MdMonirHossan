from django.urls import path
from .views import (
    InitiatePaymentView,
    FileListView, 
    TransactionListView,
    payment_success,
    payment_cancel,
    payment_failed
)

urlpatterns = [
    path('initiate-payment', InitiatePaymentView.as_view(), name='payment_initiate'),
    path('files', FileListView.as_view(), name='file_list'),
    path('transactions', TransactionListView.as_view(), name='transaction_list'),

    path('success', payment_success, name='success_page'),
    path('cancel', payment_cancel, name='cancel_page'),
    path('failed', payment_failed, name='failed_page'),
]