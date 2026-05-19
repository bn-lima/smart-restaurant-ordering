from rest_framework.generics import ListAPIView
from devices.models import Device
from .pagination import DeviceListPagination
from rest_framework import permissions, status
from .serializers import DeviceListSerializer, UpdateDeviceSerializer
from rest_framework.views import APIView
from devices.services import get_device_by_id
from rest_framework.response import Response

class DevicesList(ListAPIView): # View responsável por listar todos os dispositivos
    permission_classes = [permissions.IsAdminUser]
    serializer_class = DeviceListSerializer
    pagination_class = DeviceListPagination
    queryset = Device.objects.all()

class UpdateDevice(APIView): # View responsável por atualizar dados de um dispositivo específico
    permission_classes = [permissions.IsAdminUser]

    def patch(self, request, pk, *args, **kwargs):
        
        device = get_device_by_id(pk) # Pega o dispositivo pelo id

        if not device:
            return Response({"detail": "Device not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UpdateDeviceSerializer(data=request.data, instance=device, context={"authenticated_device": request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_200_OK)