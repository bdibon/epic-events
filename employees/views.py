from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .serializers import EmployeeSerializer


class EmployeeModelViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]
