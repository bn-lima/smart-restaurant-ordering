from rest_framework import serializers
from .models import Device
from django.conf import settings
from .validators import PASSWORD_VALIDATOR

class AuthenticateDeviceSerializer(serializers.ModelSerializer): # Serializer responsável por validar token e autenticar o dispositivo
    device_authentication_token = serializers.UUIDField(required=True) # Token de autenticação
    password = serializers.CharField(required=True, max_length=128, validators=[PASSWORD_VALIDATOR]) # Senha de usuário
    confirm_password = serializers.CharField(required=True, max_length=128, validators=[PASSWORD_VALIDATOR]) # Confirmar senha

    class Meta:
        model = Device
        fields = ("username", "password", "confirm_password", "device_authentication_token")

    def validate(self, data):

        if data[self.device_authentication_token] != settings.DEVICE_AUTHENTICATION_TOKEN: # Verifica se o token de autenticação está correto
            raise serializers.ValidationError("Invalid authentication token")
        
        if data["password"] != data[self.confirm_password]: # Verifica se as senhas batem
            raise serializers.ValidationError("Passwords do not match")
        
        return data
    
    def create(self, validated_data):
        password = validated_data.pop("password") # Remove a senha dos dados validados
        validated_data.pop("confirm_password") # Remove confirmar senha dos dados validados

        device = Device( # Cria uma instância de device
            **validated_data
        )

        device.set_password(password) # Define password de forma segura
        device.save() # Salva  device