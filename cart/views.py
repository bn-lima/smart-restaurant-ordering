from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from restaurant_menu.services import get_menu_item_by_id
from .serializers import MenuItemQuantitySerializer, AddMenuItemToCartSerializer, ShowCartSerializer
from .services import get_cart

class AddMenuItemToCart(APIView): # Serializer responsável por adicionar um item do menu no carrinho
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):

        menu_item = get_menu_item_by_id(pk) # Pega um carrinho ativo ou cria um

        if not menu_item:
            return Response({"detail": "Menu item not found"}, status=status.HTTP_404_NOT_FOUND)
        
        quantity_serializer = MenuItemQuantitySerializer(data=request.data) # Serializer responsável por validar a quantidade de itens que serão adicionados no carrinho
        quantity_serializer.is_valid(raise_exception=True)

        quantity = quantity_serializer.validated_data.get("quantity")

        cart, _ = get_cart(request.user) # Pega o carrinho referente ao dispositivo logado

        add_serializer = AddMenuItemToCartSerializer(context={"cart": cart, "menu_item": menu_item, "quantity": quantity}) # Serializer responsável por mostrar as informações do carrinho
        add_serializer.save()

        response_serializer = ShowCartSerializer(instance=cart)

        return Response(response_serializer.data)