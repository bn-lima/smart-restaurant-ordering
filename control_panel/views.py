from rest_framework.generics import ListAPIView
from devices.models import Device
from .pagination import DeviceListPagination, OrderListPagination
from rest_framework import permissions, status
from .serializers import DeviceListSerializer, UpdateDeviceSerializer, CreateDeviceSerializer, UpdateMenuItemSerializer, ConfirmationPasswordSerializier, AdminOrdersListSerializer
from rest_framework.views import APIView
from devices.services import get_device_by_id
from rest_framework.response import Response
from restaurant_menu.services import get_menu_item_by_id
from kitchen.models import Order
from django_filters.rest_framework import DjangoFilterBackend
from .filters import DeliveredOrdersFilter, PendingOrdersFilter

class DevicesList(ListAPIView): # View responsável por listar todos os dispositivos
    permission_classes = [permissions.IsAdminUser]
    serializer_class = DeviceListSerializer
    pagination_class = DeviceListPagination
    queryset = Device.objects.all()
class UpdateDevice(APIView): # View responsável por atualizar dados de um dispositivo específico
    permission_classes = [permissions.IsAdminUser]

    def patch(self, request, pk, *args, **kwargs):
        
        device = get_device_by_id(pk) # Pega o dispositivo pelo id

        if not device:
            return Response({"detail": "Device not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UpdateDeviceSerializer(data=request.data, instance=device, context={"authenticated_device": request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_200_OK)
    
class CreateDevice(APIView): # View responsável por criar um dispositivo via admin
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, *args, **kwargs):
        serializer = CreateDeviceSerializer(data=request.data, context={"super_user": request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"detail": "Device created successfully"}, status=status.HTTP_201_CREATED)

# Menu item
class UpdateMenuItem(APIView): # View responsável por atualizar dados de um item do menu
    permission_classes = [permissions.IsAdminUser]

    def patch(self, request, pk, *args, **kwargs):
        menu_item = get_menu_item_by_id(pk)

        if not menu_item: # Retorna erro caso não exista um item com esse id (pk) específico
            return Response({"detail": "Menu item not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UpdateMenuItemSerializer(instance=menu_item, data=request.data, context={"super_user":request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_200_OK)
    
class DeleteMenuItem(APIView): # View responsável por deletar um item do menu
    permission_classes = [permissions.IsAdminUser]

    def delete(self, request, pk, *args, **kwargs):
        
        menu_item = get_menu_item_by_id(pk) # Pega item do menu pelo id

        if not menu_item: # Retorna erro caso o item não exista
            return Response({"detail": "Menu item not found"}, status=status.HTTP_404_NOT_FOUND)
        
        confirmation_serializer = ConfirmationPasswordSerializier(data=request.data, context={"super_user":request.user}) # Validação da senha do super usuário
        confirmation_serializer.is_valid(raise_exception=True)

        menu_item.delete()
        
        return Response(status.HTTP_204_NO_CONTENT)
    
class DeliveredOrders(ListAPIView): # View responsável por listar os pedidos entregues
    permission_classes = [permissions.IsAdminUser]
    queryset = Order.objects.filter(delivered=True)
    pagination_class = OrderListPagination
    serializer_class = AdminOrdersListSerializer
    
    filter_backends = [DjangoFilterBackend]
    filterset_class = DeliveredOrdersFilter # Classe de filtro por data

class PendingOrders(ListAPIView): # View responsável por listar os pedidos não entregues
    permission_classes = [permissions.IsAdminUser]
    queryset = Order.objects.filter(delivered=False)
    serializer_class = AdminOrdersListSerializer
    pagination_class = OrderListPagination

    filter_backends = [DjangoFilterBackend]
    filterset_class = PendingOrdersFilter