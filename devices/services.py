from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import Device
from django.utils import timezone
from datetime import timedelta

def authenticate_device(username, password):

    device = authenticate(username=username, password=password)

    if not device:
        return None
    
    token, _ = Token.objects.get_or_create(user=device)
    return token.key

def get_device_by_username(username):
    try:
        device = Device.objects.get(username=username)
    except Device.DoesNotExist:
        return None
    return device

def block_if_attempt_limit_reached(device):

    if not device.is_blocked:

        if device.login_attempts >= 5:

            device.is_blocked = True
            device.blocked_until = timezone.now() + timedelta(minutes=15)
            device.save()

            return True
    return False

def unblock_if_expired(device):
    
    if device.blocked_until < timezone.now():

        device.is_blocked = False
        device.blocked_until = None
        device.login_attempts = 0
        device.save()

        return False

    seconds_remaining = (device.blocked_until - timezone.now()).total_seconds() / 60
    return round(seconds_remaining, 2)