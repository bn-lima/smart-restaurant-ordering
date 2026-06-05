from django.urls import path
from .views import Orders

urlpatterns = [
    path("orders/", Orders.as_view(), name="orders") # Lista todos os pedidos que não foram entregues
]