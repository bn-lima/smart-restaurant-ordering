from rest_framework.generics import ListAPIView
from devices.models import Device
from .pagination import DeviceListPagination
from rest_framework import permissions
from .serializers import DeviceListSerializer

class DevicesList(ListAPIView): # View responsável por listar todos os dispositivos
    permission_classes = [permissions.IsAdminUser]
    serializer_class = DeviceListSerializer
    pagination_class = DeviceListPagination
    queryset = Device.objects.all()