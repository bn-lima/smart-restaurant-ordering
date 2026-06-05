from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.generics import ListAPIView
from .serializers import OrdersSerializer
from .models import Order
from .pagination import OrdersPagination
from .services import get_order_by_id, deliver_order
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
    
class DeliverOrder(APIView): # View responsável por marcar um pedido como entregue
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk, *args, **kwargs):

        order = get_order_by_id(pk) # Pega o pedido com o mesmo id (pk) passado na requisição

        if not order:
            return Response({"detail": "Order object not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if order.delivered: # Retorna erro caso o pedido já tenha sido entregue
            return Response({"detail": "This order has already been delivered"}, status=status.HTTP_400_BAD_REQUEST)
        
        deliver_order(order) # Marca pedido como entregue

        return Response({"detail": "Order delivered successfully"}, status=status.HTTP_200_OK)