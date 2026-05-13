from rest_framework import serializers
from .models import Device
from django.conf import settings
from .validators import PASSWORD_VALIDATOR
from .services import authenticate_device

class AuthenticateDeviceSerializer(serializers.ModelSerializer): # Serializer responsável por validar token e autenticar o dispositivo
    device_authentication_token = serializers.UUIDField(required=True) # Token de autenticação
    password = serializers.CharField(required=True, max_length=128, validators=[PASSWORD_VALIDATOR]) # Senha de usuário
    confirm_password = serializers.CharField(required=True, max_length=128, validators=[PASSWORD_VALIDATOR]) # Confirmar senha
    class Meta:
        model = Device
        fields = ("username", "password", "confirm_password", "device_authentication_token", "function")

    def validate(self, data):

        if data["device_authentication_token"] != settings.DEVICE_AUTHENTICATION_TOKEN: # Verifica se o token de autenticação está correto
            raise serializers.ValidationError("Invalid authentication token")
        
        if data["password"] != data["confirm_password"]: # Verifica se as senhas batem
            raise serializers.ValidationError("Passwords do not match")
        
        return data
    
    def create(self, validated_data):
        password = validated_data.pop("password") # Remove a senha dos dados validados
        validated_data.pop("confirm_password") # Remove confirmar senha dos dados validados
        validated_data.pop("device_authentication_token")

        device = Device( # Cria uma instância de device
            **validated_data
        )

        device.set_password(password) # Define password de forma segura
        device.save() # Salva  device

        return device

class LoginDeviceSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, max_length=128, validators=[PASSWORD_VALIDATOR])
    device_login_token = serializers.UUIDField(required=True) # Token para validar login
    username = serializers.CharField(max_length=250, required=True)

    def validate(self, data):
        
        if data["device_login_token"] != settings.DEVICE_LOGIN_TOKEN:
            raise serializers.ValidationError("Invalid login token")
        
        token = authenticate_device(data["username"], data["password"])

        if not token:
            raise serializers.ValidationError("Invalid credentials")
        
        data["token"] = token
        return data
    
    def save(self, **kwargs):
        return self.validated_data.get("token")