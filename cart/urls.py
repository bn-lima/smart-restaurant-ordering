from django.urls import path, include
from .views import AddMenuItemToCart

urlpatterns = [
    path("item/", include([
        path("<int:pk>/", include([
            path("add/", AddMenuItemToCart.as_view(), name="add")
        ]))
    ]))
]