from rest_framework import serializers
from devices.models import Device

class DeviceListSerializer(serializers.ModelSerializer): # Serializer responsável por listar todos os dispositivos
    device_id = serializers.SerializerMethodField() # Id do dispositivo

    class Meta:
        model = Device()
        fields = ("username", "function", "device_id")

    def get_device_id(self, obj): # Retorna o id do dispositivo
        return int(obj.id)