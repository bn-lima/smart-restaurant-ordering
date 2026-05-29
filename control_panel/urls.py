from django.urls import path, include
from .views import DevicesList, UpdateDevice, CreateDevice, UpdateMenuItem

urlpatterns = [
    path("devices/", DevicesList.as_view(), name="devices"), # Lista todos os dispositivos

    path("device/", include([
        path("<int:pk>/update/", UpdateDevice.as_view(), name="update"), # Atualiza dados de um dispositivo específico,
        path("create/", CreateDevice.as_view(), name="create") # Cria um novo dispositivo via admin
    ])),

    path("item/", include([
        path("<int:pk>/update/", UpdateMenuItem.as_view(), name="update") # Atualiza dados de um item do menu
    ]))
]