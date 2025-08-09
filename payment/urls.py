from django.urls import path
from .views import FileListView, TransactionListView

urlpatterns = [
    path('files', FileListView.as_view(), name='file_list'),
    path('transactions', TransactionListView.as_view(), name='transaction_list'),
]