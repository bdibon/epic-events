from django.db import models

from clients.models import Client
from employees.models import Employee


class Event(models.Model):
    EVENT_PHASES = (
        ("S", "started"),
        ("P", "planned"),
        ("O", "over"),
    )
    name = models.CharField(max_length=128)
    attendees = models.IntegerField()
    date = models.DateField()
    status = models.CharField(max_length=1, choices=EVENT_PHASES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    support_consultant = models.ForeignKey(Employee, on_delete=models.PROTECT)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


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
