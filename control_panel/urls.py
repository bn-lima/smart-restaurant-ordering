from django.urls import path
from .views import DevicesList

urlpatterns = [
    path("devices/", DevicesList.as_view(), name="devices")
]