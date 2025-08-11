from django.contrib import admin
from .models import ActivityLog
from libs.core.admin.permissions.staff_permission import ReadOnlyForStaffMixin

# Register your models here.
@admin.register(ActivityLog)
class ActivityLogAdmin(ReadOnlyForStaffMixin, admin.ModelAdmin):
    list_display    = ('user', 'action', 'description', 'created_at')
    list_filter     = ('user', 'action')
    search_fields   = ('user__username', 'action', 'description')
    readonly_fields = ('user', 'action', 'description', 'metadata', 'created_at')