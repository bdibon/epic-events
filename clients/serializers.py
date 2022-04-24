from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import Client, Company
from employees.serializers import EmployeeSerializer
from employees.models import Employee


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ("id", "name")
        extra_kwargs = {
            "id": {"read_only": False, "required": False},
            "name": {"required": False, "validators": []},
        }


class ClientSerializer(serializers.ModelSerializer):
    sales_contact = EmployeeSerializer()
    company = CompanySerializer()

    class Meta:
        model = Client
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "mobile",
            "created_at",
            "updated_at",
            "is_prospect",
            "sales_contact",
            "company",
        )

    def validate(self, data):
        email = data.get("email")
        phone = data.get("phone")
        mobile = data.get("mobile")
        is_reachable = email or phone or mobile

        if not is_reachable:
            raise serializers.ValidationError(_("Client must be reachable."))
        return data

    def create(self, validated_data):
        sales_contact_data = validated_data.pop("sales_contact")
        sales_contact = Employee.objects.get(pk=sales_contact_data["id"])
        company = Company.get_company_by_name_or_id(
            **validated_data.pop("company")
        )

        return Client.objects.create(
            **validated_data, sales_contact=sales_contact, company=company
        )

    def update(self, instance, validated_data):
        for key in validated_data:
            if key == "company":
                company = Company.get_company_by_name_or_id(
                    **validated_data["company"]
                )
                instance.company = company
            elif key == "sales_contact":
                sales_contact = Employee.objects.get(
                    pk=validated_data["sales_contact"].get("id"),
                    role=Employee.SALES_PERSON,
                )
                instance.sales_contact = sales_contact
            else:
                setattr(instance, key, validated_data[key])

        instance.save()
        return instance
