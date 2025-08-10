from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import PaymentTransaction

def update_transaction(data, status, can_upload_file=False):
    transaction_id = data['mer_txnid']
    # Get PaymentTransaction instance by transaction id
    transaction = get_object_or_404(PaymentTransaction, transaction_id=transaction_id)
    # Update transaction and enable file upload status for user
    tran_status = transaction.status
    if tran_status not in ['success', 'failed']:
        transaction.status           = status
        transaction.can_upload_file  = can_upload_file
        transaction.complete_at      = timezone.now()
        transaction.gateway_response = data
        transaction.save()