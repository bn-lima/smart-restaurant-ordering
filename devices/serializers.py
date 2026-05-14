from rest_framework import serializers
from .models import Device
from django.conf import settings
from .validators import PASSWORD_VALIDATOR
from .services import authenticate_device
from .constants import DeviceFunction

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
class UpdateDeviceFunctionSerializer(serializers.Serializer): # Serializer responsável por mudar a função do dispositivo
    function = serializers.ChoiceField(choices=DeviceFunction.choices()) # Função do dispositivo

    def validate(self, data):
        device = self.context.get("device")

        if data["function"] == device.function: # Valida se a nova função é a mesma do dispositivo
            raise serializers.ValidationError("This device already has this function")

        return data
    
    def save(self, **kwargs):
        device = self.context.get("device")
        
        device.function = self.validated_data["function"] # Define a nova função do dispositivo
        device.save()

        return device
    
class UpdateDevicePasswordSerializer(serializers.Serializer): # Serializer responsável por atualizar a senha do dispositivo logado
    new_password = serializers.CharField(required=True, max_length=128, validators=[PASSWORD_VALIDATOR])
    confirm_new_password = serializers.CharField(required=True, max_length=128, validators=[PASSWORD_VALIDATOR])
    device_reset_password_token = serializers.UUIDField(required=True) # Token para validar reset de senha

    def validate(self, data):
        device = self.context.get("device") # Dispositivo logado
        new_password = data["new_password"]

        if data["device_reset_password_token"] != settings.DEVICE_RESET_PASSWORD_TOKEN: # Valida se o token de reset está correto
            raise serializers.ValidationError("Invalid reset token")

        if device.check_password(new_password): # Valida se a nova senha é igual a senha atual
            raise serializers.ValidationError("Your new password cannot be the same as your current password")
        
        if new_password != data["confirm_new_password"]: # verifica se as duas senhas são iguais
            raise serializers.ValidationError("Passwords do not match")
        
        return data
    
    def save(self, **kwargs):
        device = self.context.get("device")

        device.set_password(self.validated_data.get("new_password")) # Define a nova senha
        device.save()

        return device