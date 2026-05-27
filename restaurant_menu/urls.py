from django.urls import path
from .views import MenuItems

urlpatterns = [
    path("", MenuItems.as_view(), name="menu") # Mostra todos os itens ativos do menu
]
