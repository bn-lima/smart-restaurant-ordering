from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

def authenticate_device(username, password):

    device = authenticate(username=username, password=password)

    if not device:
        return None
    
    token, _ = Token.objects.get_or_create(user=device)
    return token.key