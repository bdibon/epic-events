from rest_framework.permissions import BasePermission, SAFE_METHODS

from employees.models import Employee


class ClientObjectPermissions(BasePermission):
    """
    A custom permission class that checks if the current user has the right
    permissions to perform a given action.
    This should be used with IsAutenticated permission.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        employee = request.user

        if employee.role == Employee.MANAGER:
            # A manager has the right to perform any action.
            return True

        if employee.role == Employee.SALES_PERSON:
            # A salesperson might have the right to perform any action on a client.
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        employee = request.user

        if employee.role == Employee.MANAGER:
            return True

        if employee.role == Employee.SALES_PERSON:
            return obj.sales_contact == employee

        return False
