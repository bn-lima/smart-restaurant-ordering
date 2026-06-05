from rest_framework import serializers
from .models import Order
from cart.models import Cart, CartItem

class ShowOrderCartItemsSerializer(serializers.ModelSerializer): # Serializer responsável por exibir os itens do carrinho de um pedido
    menu_item_name = serializers.SerializerMethodField() # Nome do item do cardápio
    menu_item_description = serializers.SerializerMethodField() # Descrição do item do cardápio
    menu_item_ingredients = serializers.SerializerMethodField() # Ingredientes do item do cardápio
    menu_item_image = serializers.ImageField(source="menu_item.item_image") # Imagem do item do cardápio

    class Meta:
        model = CartItem
        fields = ("menu_item", "menu_item_image", "menu_item_name", "menu_item_description", "menu_item_ingredients", "quantity")

    def get_menu_item_name(self, obj): # Retorna o nome do item do cardápio
        return obj.menu_item.item_name
    
    def get_menu_item_description(self, obj): # Retorna a descrição do item do cardápio
        return obj.menu_item.item_description
    
    def get_menu_item_ingredients(self, obj): # Retorna os ingredientes do item do cardápio
        return obj.menu_item.item_ingredients

class ShowCartOrderSerializer(serializers.ModelSerializer): # Serializer responsável por exibir o carrinho associado ao pedido
    items = ShowOrderCartItemsSerializer(many=True) # Lista de itens presentes no carrinho

    class Meta:
        model = Cart
        fields = ("items",)

class OrdersSerializer(serializers.ModelSerializer): # Serializer responsável por serializar os pedidos ainda não entregues
    cart = ShowCartOrderSerializer()

    class Meta:
        model = Order
        exclude = ("delivered_at", "delivered")

    def to_representation(self, instance): # Renomeia o campo "cart" para "order" na resposta da API
        data = super().to_representation(instance)

        data["order"] = data.pop("cart")
        return data