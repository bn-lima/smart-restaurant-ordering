from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from .serializers import AuthenticateDeviceSerializer, LoginDeviceSerializer, UpdateDeviceFunctionSerializer, UpdateDevicePasswordSerializer

class AuthenticateDevice(APIView): # View responsável por autenticar um dispositivo
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):

        serializer = AuthenticateDeviceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"detail": "Device registered successfully"}, status=status.HTTP_201_CREATED)
class LoginDevice(APIView): # View responsável por realizar o login do dispositivo
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginDeviceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token_key = serializer.save()

        return Response({"login_token": token_key}, status=status.HTTP_200_OK)
class UpdateDevicePassword(APIView): # View responsável por atualizar a senha do dispositivo logado
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = UpdateDevicePasswordSerializer(data=request.data, context={"device": request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"detail": "Password updated successfully"}, status=status.HTTP_200_OK)
class UpdateDeviceFunction(APIView): # View responsável por mudar a função do dispositivo
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        serializer = UpdateDeviceFunctionSerializer(data=request.data, context={"device": request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"detail": "Device function updated successfully"}, status=status.HTTP_200_OK)