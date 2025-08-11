from django.contrib import messages

class ReadOnlyForStaffMixin:
    """
    A mixin for Django admin to restrict delete and update permissions for staff.

    The mixin ensured that only superusers have the ability to delete or update.
    """

    def has_module_permission(self, request):
        # staff can see the app in the admin menu
        return True

    def has_view_permission(self, request, obj=None):
        """
        Allow staff to view but not edit/delete. Superusers can do anything.
        """
        if request.user.is_superuser:
            return True
        if request.user.is_staff:
            return True
        return False

    def has_add_permission(self, request):
        """
        Denies add permission for staff (non-superuser)

        Returns: 
            bool: True for superuser, False otherwise
        """
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        """
        Denies update permission for staff (non-superuser)

        Returns: 
            bool: True for superuser, False otherwise
        """
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        """
        Denies delete permission for all staff (non-superuser)

        Returns:
            bool: True if the user is a superuser False otherwise.
        """
        return request.user.is_superuser