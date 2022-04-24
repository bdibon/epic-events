from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from clients.models import Client
from employees.models import Employee


class Event(models.Model):
    EVENT_STARTED = "S"
    EVENT_PLANNED = "P"
    EVENT_OVER = "O"
    EVENT_DRAFT = "D"
    EVENT_PHASES = (
        (EVENT_STARTED, "started"),
        (EVENT_PLANNED, "planned"),
        (EVENT_OVER, "over"),
        (EVENT_DRAFT, "draft"),
    )
    name = models.CharField(max_length=128)
    attendees = models.IntegerField()
    date = models.DateField()
    status = models.CharField(
        max_length=1, choices=EVENT_PHASES, default=EVENT_DRAFT
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    support_consultant = models.ForeignKey(Employee, on_delete=models.PROTECT)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        contract = getattr(self, "contract", None)

        if contract is None:
            if self.status != self.EVENT_DRAFT:
                raise ValidationError(
                    _("An event with no contract has to be a draft.")
                )
        else:
            if contract.client != self.client:
                raise ValidationError(
                    _(
                        "The event's client must be the same as the contract's client."
                    )
                )
        super().save(*args, **kwargs)


class Contract(models.Model):
    status = models.BooleanField(default=False)
    amount = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    sales_person = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        limit_choices_to={"role": Employee.SALES_PERSON},
    )
    event = models.OneToOneField(
        Event,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    class Meta:
        constraints = [
            # When a contract is signed, make sure a related event is created.
            models.CheckConstraint(
                check=(
                    models.Q(status__exact=False)
                    & models.Q(event__isnull=True)
                )
                | (
                    models.Q(status__exact=True)
                    & models.Q(event__isnull=False)
                ),
                name="status_match_event",
            )
        ]

    def __str__(self):
        return (
            f"{self.client.company.name} - "
            f"{self.client} / {self.sales_person}"
        )
