from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

SALES_PERSON = "SP"
SUPPORT_CONSULTANT = "SC"
MANAGER = "M"

ROLE_GROUP_MAP = {
    SALES_PERSON: "sales",
    SUPPORT_CONSULTANT: "support",
    MANAGER: "management",
}


class EmployeeManager(BaseUserManager):
    def create_user(self, email, role, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Employee must have is_staff=True"))
        if not email:
            raise ValueError(_("The email must be set."))

        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True"))

        user = self.create_user(
            email, Employee.MANAGER, password=password, **extra_fields
        )
        user.save(using=self._db)
        return user


class Employee(AbstractUser):
    SALES_PERSON = SALES_PERSON
    SUPPORT_CONSULTANT = SUPPORT_CONSULTANT
    MANAGER = MANAGER

    ROLE_CHOICES = (
        (SALES_PERSON, _("Salesperson")),
        (SUPPORT_CONSULTANT, _("Support consultant")),
        (MANAGER, _("Manager")),
    )

    username = None
    email = models.EmailField(_("email address"), unique=True)
    role = models.CharField(max_length=2, choices=ROLE_CHOICES)
    is_staff = models.BooleanField(
        _("staff status"),
        default=True,
        help_text=_(
            "Designates whether the user can log into this admin site."
        ),
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = EmployeeManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        group = Group.objects.get(name=ROLE_GROUP_MAP[self.role])
        self.groups.add(group)
