from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from employees.models import Employee


class Company(models.Model):
    name = models.CharField(max_length=140)

    class Meta:
        verbose_name_plural = "companies"

    def __str__(self):
        return self.name


class Client(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    phone = PhoneNumberField(blank=True)
    mobile = PhoneNumberField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_prospect = models.BooleanField(default=True)

    sales_contact = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        limit_choices_to={"role": Employee.SALES_PERSON},
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(email__isnull=False)
                | models.Q(phone__isnull=False)
                | models.Q(mobile__isnull=False),
                name="is_reachable",
            ),
        ]

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name
