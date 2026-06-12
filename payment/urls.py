from django.urls import path
from .views import MPPayment, WebHook

urlpatterns = [
    path("payment/", MPPayment.as_view(), name="payment"),
    path("webhook/", WebHook.as_view(), name="webhook")
]