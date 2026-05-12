from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from serializers import AuthenticateDeviceSerializer

class AuthenticateDevice(APIView): # View responsável por autenticar um dispositivo (Verificar se é preciso mudar o nome dps)
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):

        serializer = AuthenticateDeviceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"detail": "Device registered successfully"}, status=status.HTTP_201_CREATED)