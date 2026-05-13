from django.urls import path, include
from .views import AuthenticateDevice, LoginDevice, UpdateDeviceFunction

urlpatterns = [
    path("authenticate/", AuthenticateDevice.as_view(), name="authenticate"),
    path("login/", LoginDevice.as_view(), name="login"),

    path("update/", include([
        path("function/", UpdateDeviceFunction.as_view(), name="function")
    ]))
]