from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.generics import ListAPIView
from .serializers import OrdersSerializer
from .models import Order
from .pagination import OrdersPagination
from cart.services import get_cart

class Orders(ListAPIView): # View responsável por retornar uma lista de pedidos ainda não entregues
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrdersSerializer
    pagination_class = OrdersPagination

    def list(self, request, *args, **kwargs):

        if request.user.function == "checkout": # Verifica se a função do dispositivo tem permissão para ver os pedidos
            return Response({"detail": "You do not have permission to access this endpoint"}, status=status.HTTP_200_OK)
        
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        return Order.objects.filter(delivered=False).order_by("created_at") # Retorna os pedidos não entregues, ordenados do mais recente para o mais antigo