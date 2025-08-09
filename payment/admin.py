from django.contrib import admin
from .models import FileUpload, PaymentTransaction

# Register your models here.
@admin.register(FileUpload)
class FileUploadAdmin(admin.ModelAdmin):
    list_display    = ('user', 'filename', 'status', 'word_count', 'created_at')
    list_filter     = ('filename', 'user', 'status')
    search_fields   = ('filename', 'user__username', 'status')


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display    = ('user', 'transaction_id', 'amount', 'status', 'created_at')
    list_filter     = ('transaction_id', 'user', 'status')
    search_fields   = ('transaction_id', 'user__username', 'status')
