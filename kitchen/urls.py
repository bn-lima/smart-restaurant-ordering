from django.urls import path, include
from .views import Orders, DeliverOrder

urlpatterns = [
    path("orders/", Orders.as_view(), name="orders"), # Lista todos os pedidos que não foram entregues

    path("order/", include([
        path("<int:pk>/", include([
            path("deliver/", DeliverOrder.as_view(), name="deliver")
        ]))
    ]))
]