from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import Contract, Event
from employees.models import Employee


class EventSerializer(serializers.ModelSerializer):
    support_consultant = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.filter(role=Employee.SUPPORT_CONSULTANT)
    )
    contract = serializers.PrimaryKeyRelatedField(
        allow_null=True, read_only=True
    )

    class Meta:
        model = Event
        fields = "__all__"

    def validate_client(self, value):
        if self.instance is not None and self.instance._state.adding is False:
            contract = getattr(self.instance, "contract", None)
            if contract and contract.client != value:
                raise serializers.ValidationError(
                    _(
                        "The event's client must be the same as the contract's client."
                    )
                )

        return value

    def validate_status(self, value):
        if self.instance is None and value != Event.EVENT_DRAFT:
            raise serializers.ValidationError(
                _("Event not bound to a contract has to be a draft.")
            )
        return value


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = "__all__"

    def validate(self, attrs):
        status = attrs.get("status", None)
        event = attrs.get("event", None)

        if event is not None and status is False:
            raise serializers.ValidationError(
                "A contract with an associated event must be signed."
            )
        return attrs
