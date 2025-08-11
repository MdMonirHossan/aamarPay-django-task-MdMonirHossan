from django.contrib import admin
from .models import FileUpload, PaymentTransaction
from libs.utils.permissions.staff_permission import ReadOnlyForStaffMixin

# Register your models here.
@admin.register(FileUpload)
class FileUploadAdmin(admin.ModelAdmin):
    """
    Admin configuration for FileUpload model.
    """
    list_display    = ('user', 'filename', 'status', 'word_count', 'upload_time')
    list_filter     = ('filename', 'user', 'status')
    search_fields   = ('filename', 'user__username', 'status')
    # readonly_fields = ('user', 'file', 'filename', 'status', 'word_count', 'created_at')


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    """
    Admin configuration for PaymentTransaction model.
    """
    list_display    = ('user', 'transaction_id', 'amount', 'status', 'can_upload_file', 'completed_at', 'created_at')
    list_filter     = ('transaction_id', 'user', 'status')
    search_fields   = ('transaction_id', 'user__username', 'status')
    # readonly_fields = ('user', 'transaction_id', 'amount', 'status', 'gateway_response', 'created_at')
