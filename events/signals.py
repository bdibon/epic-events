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


@receiver(post_save, sender=Contract)
def sync_contract_client_with_event(sender, **kwargs):
    """
    Make sure that when a signed contract's client is changed,
    this applies to the related event.
    """
    contract = kwargs["instance"]

    if contract.status:
        event = contract.event
        if event.client != contract.client:
            event.client = contract.client
            event.save()
