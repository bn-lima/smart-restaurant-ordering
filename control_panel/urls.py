from django.urls import path, include
from .views import DevicesList, UpdateDevice, CreateDevice, UpdateMenuItem, DeleteMenuItem, DeliveredOrders

urlpatterns = [
    path("devices/", DevicesList.as_view(), name="devices"), # Lista todos os dispositivos

    path("device/", include([
        path("<int:pk>/update/", UpdateDevice.as_view(), name="update"), # Atualiza dados de um dispositivo específico,
        path("create/", CreateDevice.as_view(), name="create") # Cria um novo dispositivo via admin
    ])),

    path("item/", include([
        path("<int:pk>/", include([
            path("update/", UpdateMenuItem.as_view(), name="update"), # Atualiza dados de um item do menu
            path("delete/", DeleteMenuItem.as_view(), name="delete") # Deleta um item do menu
        ])),
    ])),
    
    path("orders/", include([
        path("delivered/", DeliveredOrders.as_view(), name="delivered")
    ]))
]