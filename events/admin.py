import copy
import datetime

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm, ValidationError


from .models import Contract, Event
from employees.models import Employee
from clients.models import Client


class ContractAdminForm(ModelForm):
    class Meta:
        model = Contract
        fields = ("client", "sales_person", "amount", "status", "event")

    def clean(self):
        cleaned_data = super().clean()

        # Deal with the contract status and event constraint.
        contract_status = cleaned_data["status"]
        related_event = cleaned_data["event"]

        if contract_status is False and related_event is not None:
            raise ValidationError(
                _(
                    "Unless the contract is signed, it should not have a related event."  # NOQA
                )
            )
        if contract_status is True and related_event is None:
            raise ValidationError(
                _("A signed contract must have a related event.")
            )

        # Prevent other salespersons to sign the contract.
        client = cleaned_data["client"]
        sales_person = cleaned_data["sales_person"]
        if client.sales_contact != sales_person:
            raise ValidationError(
                _(
                    "The client that signs the contract with the salesperson must be in his portfolio."  # NOQA
                )
            )
        return cleaned_data


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = (
        "event",
        "get_company",
        "client",
        "sales_person",
        "amount",
        "status",
    )
    list_filter = ("client__company", "status")
    search_fields = (
        "client__company__name",
        "client__first_name",
        "client__last_name",
        "sales_person__email",
    )
    form = ContractAdminForm

    @admin.display(description=_("Company"))
    def get_company(self, obj):
        return obj.client.company.name

    def has_change_permission(self, request, obj=None):
        if request.user.role == Employee.MANAGER:
            return True

        if request.user.role == Employee.SALES_PERSON:
            if obj is None:
                return False
            if obj.sales_person == request.user:
                return True
            return False

        return False

    def get_form(self, request, obj=None, **kwargs):
        base_form = super().get_form(request, obj, **kwargs)
        form = copy.deepcopy(base_form)

        if (
            request.user.role == Employee.SALES_PERSON
            and "sales_person" in form.base_fields
        ):
            if obj is None:
                form.base_fields["sales_person"].initial = request.user
            form.base_fields["sales_person"].disabled = True
            form.base_fields["client"].queryset = Client.objects.filter(
                sales_contact=request.user
            )

        return form


class EventAdminForm(ModelForm):
    class Meta:
        model = Event
        fields = (
            "name",
            "attendees",
            "date",
            "status",
            "support_consultant",
            "client",
        )

    def clean_date(self):
        date = self.cleaned_data["date"]

        if date < datetime.date.today():
            raise ValidationError(
                _("You cannot set an event's date in the past.")
            )

        return date

    def clean_status(self):
        status = self.cleaned_data["status"]
        draft_error = ValidationError(
            _("An event without a contract has to be a draft.")
        )

        if self.instance._state.adding is True:
            if status != Event.EVENT_DRAFT:
                raise draft_error
        else:
            contract = getattr(self.instance, "contract", None)

            if contract is None and status != Event.EVENT_DRAFT:
                raise draft_error

        return status

    def clean_client(self):
        client = self.cleaned_data["client"]
        contract = getattr(self.instance, "contract", None)

        if contract is not None:
            if client != contract.client:
                raise ValidationError(
                    _(
                        "Event's client must be the same as the contract's client."
                    )
                )
        return client


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "get_company",
        "date",
        "attendees",
        "status",
        "support_consultant",
    )
    list_filter = ("client__company",)
    search_fields = (
        "name",
        "client__company__name",
        "support_consultant__email",
    )
    form = EventAdminForm

    @admin.display(description=_("Company"))
    def get_company(self, obj):
        return obj.client.company.name

    def has_change_permission(self, request, obj=None):
        current_user = request.user

        if current_user.role == Employee.MANAGER:
            return True

        if current_user.role == Employee.SALES_PERSON:
            if obj is None:
                return False
            if getattr(obj, "contract", None) is not None:
                return obj.contract.sales_person == current_user
            else:
                return True

        if current_user.role == Employee.SUPPORT_CONSULTANT:
            if obj is None:
                return False
            else:
                return obj.support_consultant == current_user
        return False

    def get_form(self, request, obj=None, **kwargs):
        base_form = super().get_form(request, obj, **kwargs)
        form = copy.deepcopy(base_form)

        if "support_consultant" in form.base_fields:
            form.base_fields[
                "support_consultant"
            ].queryset = Employee.objects.filter(
                role=Employee.SUPPORT_CONSULTANT
            )

        current_user = request.user
        if (
            current_user.role == Employee.SALES_PERSON
            and "client" in form.base_fields
        ):
            form.base_fields["client"].queryset = Client.objects.filter(
                sales_contact=current_user
            )

        return form
