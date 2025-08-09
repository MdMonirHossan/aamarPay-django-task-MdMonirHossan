from django.contrib import admin
from .models import FileUpload

# Register your models here.
@admin.register(FileUpload)
class FileUploadAdmin(admin.ModelAdmin):
    list_display    = ('user', 'filename', 'status', 'word_count', 'created_at')
    list_filter     = ('filename', 'user', 'status')
    search_fields   = ('filename', 'user__username', 'status')
