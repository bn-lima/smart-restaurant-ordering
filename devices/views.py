from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from .serializers import AuthenticateDeviceSerializer, LoginDeviceSerializer

class AuthenticateDevice(APIView): # View responsável por autenticar um dispositivo (Verificar se é preciso mudar o nome dps)
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):

        serializer = AuthenticateDeviceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"detail": "Device registered successfully"}, status=status.HTTP_201_CREATED)
    
class LoginDevice(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginDeviceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token_key = serializer.save()

        return Response({"login_token": token_key}, status=status.HTTP_200_OK)