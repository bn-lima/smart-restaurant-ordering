from django.urls import path
from .views import MPPayment

urlpatterns = [
    path("payment/", MPPayment.as_view(), name="payment")
]