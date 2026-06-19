from django.db import models
from django.contrib.auth.models import AbstractUser
from .constants import DeviceFunction
class Device(AbstractUser):
    function = models.CharField(max_length=10, choices=DeviceFunction.choices()) # Campo que representa a função que o dispositivo vai realizar no restaurante
    point_terminal_id = models.CharField(max_length=255, blank=True, null=True) # Id da maquininha de pagamento 

    USERNAME_FIELD = "username"

    def __str__(self):
        return str(self.username)