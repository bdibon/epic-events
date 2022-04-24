from rest_framework import viewsets, permissions


from .models import Event, Contract
from .serializers import ContractSerializer, EventSerializer
from .permissions import EventObjectPermissions, ContractObjectPermissions


class EventsViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    permission_classes = [permissions.IsAuthenticated, EventObjectPermissions]


class ContractsViewSet(viewsets.ModelViewSet):
    serializer_class = ContractSerializer
    queryset = Contract.objects.all()
    permission_classes = [
        permissions.IsAuthenticated,
        ContractObjectPermissions,
    ]
