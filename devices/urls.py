from django.urls import path, include
from .views import AuthenticateDevice,LoginDevice

urlpatterns = [
    path("authenticate/", AuthenticateDevice.as_view(), name="authenticate"),
    path("login/", LoginDevice.as_view(), name="login")
]