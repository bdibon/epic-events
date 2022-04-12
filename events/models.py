from django.db import models

from clients.models import Client
from employees.models import Employee


class Event(models.Model):
    EVENT_PHASES = (
        ("S", "started"),
        ("P", "planned"),
        ("O", "over"),
    )

    attendees = models.IntegerField()
    date = models.DateField()
    status = models.CharField(max_length=1, choices=EVENT_PHASES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    support_consultant = models.ForeignKey(Employee, on_delete=models.PROTECT)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)


class Contract(models.Model):
    # When a contract is signed, make sure a related event is created
    status = models.BooleanField(default=False)
    amount = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # When a contract is created, make sure the client's  is_prospect attribute is set to False
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    sales_person = models.ForeignKey(Employee, on_delete=models.PROTECT)
    event = models.ForeignKey(Event, on_delete=models.PROTECT, null=True)
