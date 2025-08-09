from django.contrib import messages

class ReadOnlyForStaffMixin:
    """
    A mixin for Django admin to restrict delete and update permissions for staff.

    The mixin ensured that only superusers have the ability to delete or update.
    """
    # def get_readonly_fields(self, request, obj=None):
    #     if not request.user.is_superuser:
    #         return [field.name for field in obj._meta.fields]
    #     return super().get_readonly_fields(request, obj)

    def has_view_permission(self, request, obj=None):
        """
        Allow all users superuser/staff to view the models.
        """
        return request.user.is_staff or request.user.is_superuser
    
    def has_add_permission(self, request, obj=None):
        # if request.user.is_superuser:
        #     return True
        # # else:
        #     self.message_user(request, "You don't have permission to add.", level='error')
        # return super().has_add_permission(request)
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        """
        Denies delete permission for all staff (non-superuser)

        Returns:
            bool: True if the user is a superuser False otherwise.
        """
        # if not request.user.is_superuser:
        #     return False
        # else:
        #     self.message_user(request, "You don't have permission to delete.", level='error')
        # return super().has_delete_permission(request, obj)
        return request.user.is_superuser
    
    def has_change_permission(self, request, obj=None):
        """
        Denies update permission for staff (non-superuser)

        Returns: 
            bool: True for superuser, False otherwise
        """
        # if not request.user.is_superuser:
        #     return False
        # else:
        #     self.message_user(request, "You don't have permission to edit.", level='error')
        # return super().has_change_permission(request, obj)
        return request.user.is_superuser

    def get_readonly_fields(self, request, obj=None):
        """
        Makes all fields read-only for staff users in admin form
        """
        if not request.user.is_superuser:
            return [field.name for field in self.model._meta.fields]
        return super().get_readonly_fields(request, obj)