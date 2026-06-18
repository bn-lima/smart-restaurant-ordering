from django.urls import path, include
from .views import MenuItems, MenuItemDetail

urlpatterns = [
    path("", MenuItems.as_view(), name="menu"), # Mostra todos os itens ativos do menu

    path("item/", include([
        path("<int:pk>/detail/", MenuItemDetail.as_view(), name="detail")
    ]))
]