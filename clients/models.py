from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from employees.models import Employee


class Company(models.Model):
    name = models.CharField(max_length=140, unique=True)

    class Meta:
        verbose_name_plural = "companies"

    def __str__(self):
        return self.name

    @classmethod
    def get_company_by_name_or_id(cls, **kwargs):
        pk = kwargs.pop("id", None)
        name = kwargs.pop("name", None)

        if pk:
            return cls.objects.get(pk=pk)
        if name:
            company, created = cls.objects.get_or_create(name=name)
            return company

        return None


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
                check=~models.Q(email__exact="")
                | ~models.Q(phone__exact="")
                | ~models.Q(mobile__exact=""),
                name="is_reachable",
            ),
        ]

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name
