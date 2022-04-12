from django.contrib import admin

from .models import Client, Company
from employees.models import Employee


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("full_name", "company", "sales_contact", "is_prospect")
    list_filter = ("is_prospect",)
    search_fields = ("company__name", "sales_contact__email")

    def has_change_permission(self, request, obj=None):
        if request.user.role == Employee.MANAGER:
            return True

        if request.user.role == Employee.SALES_PERSON:
            if obj is None:
                return False
            if obj.sales_contact == request.user:
                return True
            return False

        return False

    def has_delete_permission(self, request, obj=None):
        return self.has_change_permission(request, obj)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    search_fields = ("name",)
