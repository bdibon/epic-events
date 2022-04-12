from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import Employee


class EmployeeCreationForm(UserCreationForm):
    """
    A form for adding new employees.
    """

    username = None

    class Meta:
        model = Employee
        fields = ("email", "role", "first_name", "last_name", "is_active")


@admin.register(Employee)
class EmployeeAdmin(UserAdmin):
    add_form = EmployeeCreationForm
    list_display = ("email", "role")
    list_filter = ("role", "is_active")
    ordering = ("email",)
    fieldsets = (
        (None, {"fields": ("first_name", "last_name", "role")}),
        (_("Credentials"), {"fields": ("email", "password")}),
        (None, {"fields": ("is_active",)}),
    )
    add_fieldsets = (
        (None, {"fields": ("first_name", "last_name", "role")}),
        (_("Credentials"), {"fields": ("email", "password1", "password2")}),
        (None, {"fields": ("is_active",)}),
    )
    search_fields = ("email", "first_name", "last_name")
