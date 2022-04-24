from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Event, Contract
from .serializers import ContractSerializer, EventSerializer
from .permissions import EventObjectPermissions, ContractObjectPermissions
from .filters import ContractFilter, EventFilter


class EventsViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    permission_classes = [permissions.IsAuthenticated, EventObjectPermissions]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = EventFilter
    search_fields = ["client__last_name", "client__email", "date"]


class ContractsViewSet(viewsets.ModelViewSet):
    serializer_class = ContractSerializer
    queryset = Contract.objects.all()
    permission_classes = [
        permissions.IsAuthenticated,
        ContractObjectPermissions,
    ]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ContractFilter
    search_fields = [
        "client__last_name",
        "client__email",
        "created_at",
        "amount",
    ]
