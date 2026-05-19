from django.urls import path, include
from .views import DevicesList, UpdateDevice

urlpatterns = [
    path("devices/", DevicesList.as_view(), name="devices"), # Lista todos os dispositivos

    path("device/<int:pk>/", include([
        path("update/", UpdateDevice.as_view(), name="update") # Atualiza dados de um dispositivo específico
    ]))
]