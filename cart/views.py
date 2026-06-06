from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.generics import RetrieveAPIView
from restaurant_menu.services import get_menu_item_by_id
from .serializers import MenuItemQuantitySerializer, AddMenuItemToCartSerializer, ShowCartSerializer, RemoveMenuItemFromCartSerializer
from .services import get_cart, cancel_cart
from .models import Cart
class AddMenuItemToCart(APIView): # Serializer responsável por adicionar um item do menu no carrinho
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):

        menu_item = get_menu_item_by_id(pk) # Pega um carrinho ativo ou cria um

        if not menu_item:
            return Response({"detail": "Menu item not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if not menu_item.active:
            return Response({"This item is not active"}, status=status.HTTP_400_BAD_REQUEST)
        
        quantity_serializer = MenuItemQuantitySerializer(data=request.data) # Serializer responsável por validar a quantidade de itens que serão adicionados no carrinho
        quantity_serializer.is_valid(raise_exception=True)

        quantity = quantity_serializer.validated_data.get("quantity")

        cart, _ = get_cart(request.user) # Pega o carrinho referente ao dispositivo logado

        add_serializer = AddMenuItemToCartSerializer(data={}, context={"cart": cart, "menu_item": menu_item, "quantity": quantity}) # Serializer responsável por mostrar as informações do carrinho
        add_serializer.is_valid(raise_exception=True)
        add_serializer.save()

        response_serializer = ShowCartSerializer(instance=cart)

        return Response({"detail": "Item quantity updated", "cart": response_serializer.data}, status=status.HTTP_200_OK)
class RemoveMenuItemFromCart(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk, *args, **kwargs):
        
        menu_item = get_menu_item_by_id(pk) # Pega o item do menu

        if not menu_item:
            return Response({"detail": "Menu item not found"}, status=status.HTTP_404_NOT_FOUND)
        
        quantity_serializer = MenuItemQuantitySerializer(data=request.data) # Serializer responsável por validar a quantidade de itens que serão removidos do carrinho
        quantity_serializer.is_valid(raise_exception=True)
        
        quantity = quantity_serializer.validated_data.get("quantity")

        cart, _ = get_cart(request.user) # Pega o carrinho referente ao dispositivo logado

        remove_serializer = RemoveMenuItemFromCartSerializer(data={}, context={"cart": cart, "menu_item": menu_item, "quantity": quantity}) # Serializer responsável por remover os itens do carrinho
        remove_serializer.is_valid(raise_exception=True)

        cart_item = remove_serializer.save()

        response_serializer = ShowCartSerializer(instance=cart) # Serializa o carrinho para resposta

        if not cart_item: # Verifica se o item foi atualizado ou completamente removido
            return Response({"detail": "The item has been completely removed from your cart", "cart": response_serializer.data}, status=status.HTTP_200_OK)
        return Response({"detail": "Item quantity updated", "cart": response_serializer.data}, status=status.HTTP_200_OK)
class CancelCart(APIView): # View responsável por cancelar um carrinho ativo
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):

        cart, _ = get_cart(request.user) # Pega o carrinho ativo

        if not cart.items.all().exists(): # Verifica se o carrinho está vazio
            return Response({"detail": "You cannot cancel an empty cart"}, status=status.HTTP_400_BAD_REQUEST)
        
        cancel_cart(cart) # Cancela o carrinho

        return Response({"detail": "Cart canceled successfully"}, status=status.HTTP_200_OK)
class CartDetail(APIView): # View responsável por mostrar os detalhes de um carrinho específico
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        
        cart, _ = get_cart(request.user)

        response_serializer = ShowCartSerializer(data={},instance=cart)
        response_serializer.is_valid(raise_exception=True)

        return Response(response_serializer.data, status=status.HTTP_200_OK)