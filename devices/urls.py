from django.urls import path, include
from .views import AuthenticateDevice

urlpatterns = [
    path("authenticate/", AuthenticateDevice.as_view(), name="authenticate")
]