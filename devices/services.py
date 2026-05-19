from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import Device

def authenticate_device(username, password):

    device = authenticate(username=username, password=password)

    if not device:
        return None
    
    token, _ = Token.objects.get_or_create(user=device)
    return token.key

def get_device_by_id(id):
    try:
        device = Device.objects.get(id=id)
    except Device.DoesNotExist:
        return None
    return device