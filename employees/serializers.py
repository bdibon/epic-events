from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict
from rest_framework import serializers


from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    """
    This class should only be used for read operations or to support
    the creation / update of another model instance.
    """

    email = serializers.EmailField(required=False)
    role = serializers.ChoiceField(
        required=False, choices=Employee.ROLE_CHOICES
    )
    id = serializers.IntegerField(read_only=False)

    class Meta:
        model = get_user_model()
        fields = ("id", "first_name", "last_name", "email", "role")

    def to_internal_value(self, data):
        if isinstance(data, Employee):
            return super().to_internal_value(model_to_dict(data))

        return super().to_internal_value(data)
