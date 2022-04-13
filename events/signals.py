from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Contract


@receiver(post_save, sender=Contract)
def upgrade_prospect_to_client(sender, **kwargs):
    contract = kwargs["instance"]

    if contract.status is True:
        client = contract.client
        if client.is_prospect is True:
            client.is_prospect = False
            client.save()
