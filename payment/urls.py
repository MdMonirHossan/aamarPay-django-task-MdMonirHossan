from django.urls import path
from .views import (
    FileListView, 
    TransactionListView, 
    payment_success,
    payment_cancel
)

urlpatterns = [
    path('files', FileListView.as_view(), name='file_list'),
    path('transactions', TransactionListView.as_view(), name='transaction_list'),

    path('success', payment_success, name='success_page'),
    path('cancel', payment_cancel, name='cancel_page'),
]