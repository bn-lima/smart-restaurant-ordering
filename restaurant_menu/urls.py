from django.urls import path, include
from .views import MenuItems, CreateMenuItem

urlpatterns = [
    path("", MenuItems.as_view(), name="menu"), # Mostra todos os itens ativos do menu

    path("item/", include([
        path("create/", CreateMenuItem.as_view(), name="create") # Cria um novo item no menu
    ]))
]
