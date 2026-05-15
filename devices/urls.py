from django.urls import path, include
from .views import RegisterDevice, LoginDevice, UpdateDeviceFunction, UpdateDevicePassword, CreateAdminUser

urlpatterns = [
    path("register/", include([ # Registros
        path("", RegisterDevice.as_view(), name="authenticate"), # Registra usuário normal
        path("admin/", CreateAdminUser.as_view(), name="admin") # Registra super usuário
    ])),

    path("update/", include([
        path("function/", UpdateDeviceFunction.as_view(), name="function"), # Atualiza a função do dispositivo
        path("password/", UpdateDevicePassword.as_view(), name="password")  # Atualiza senha
    ])),

    path("login/", LoginDevice.as_view(), name="login"), # Faz login do dispositivo
]