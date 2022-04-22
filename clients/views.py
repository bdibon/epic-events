from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from .models import Client
from .serializers import ClientSerializer
from .permissions import ClientObjectPermissions
from employees.models import Employee


class ClientModelViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated, ClientObjectPermissions]

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.role == Employee.SALES_PERSON:
            request.data["sales_contact"] = user

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
