from django.urls import path, include
from .views import AddMenuItemToCart, RemoveMenuItemFromCart, CancelCart, CartDetail

urlpatterns = [
    path("cancel/", CancelCart.as_view(), name="cancel"), # Cancela o carrinho
    path("detail/", CartDetail.as_view(), name="detail"), # Mostra os detalhes do carrinho

    path("item/", include([
        path("<int:pk>/", include([
            path("add/", AddMenuItemToCart.as_view(), name="add"), # Adiciona item específico no carrinho
            path("remove/", RemoveMenuItemFromCart.as_view(), name="remove") # Remove item específico do carrinho
        ]))
    ]))
]