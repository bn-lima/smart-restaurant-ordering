from rest_framework import serializers
from .models import CartItem, Cart
from .services import is_item_in_cart
from decimal import Decimal
class MenuItemQuantitySerializer(serializers.Serializer):
    quantity = serializers.IntegerField(default=1, min_value=1)

class AddMenuItemToCartSerializer(serializers.Serializer):
    
    def save(self, **kwargs):
        cart = self.context.get("cart")
        quantity = self.context.get("quantity")
        menu_item = self.context.get("menu_item")

        cart_item = is_item_in_cart(cart, menu_item)

        if not cart_item:
            cart_item = CartItem.objects.create(cart=cart, menu_item=menu_item, quantity=quantity)

        else:
            cart_item.quantity += quantity
            cart_item.save()
            
        return cart_item
class ShowCartItemsSerializer(serializers.ModelSerializer): # Serializer responsável por exibir os itens do carrinho
    menu_item_name = serializers.SerializerMethodField() # Nome do item do carrinho
    menu_item_unit_price = serializers.SerializerMethodField() # Preço unitário do item do carrinho
    menu_item_subtotal = serializers.SerializerMethodField() # Subtotal do item do carrinho
    class Meta:
        model = CartItem
        exclude = ("cart",)

    def get_menu_item_subtotal(self, obj): # Pega o subtotal de cada item e retorna em decimal
        return (obj.get_subtotal().quantize(Decimal("0.01")))

    def get_menu_item_unit_price(self, obj): # Pega o preço unitário de cada item e retorna em decimal
        return (obj.menu_item.item_price.quantize(Decimal("0.01")))

    def get_menu_item_name(self, obj): # Pega o nome de cada item
        return obj.menu_item.item_name
class ShowCartSerializer(serializers.ModelSerializer): # Serializer responsável por exibir as informações do carrinho
    items = ShowCartItemsSerializer(many=True) # itens do carrinho
    cart_total = serializers.SerializerMethodField() # Total do carrinho
    class Meta:
        model = Cart
        exclude = ("device",)

    def get_cart_total(self, obj): # Pega o total do carrinho
        return (obj.get_total().quantize(Decimal("0.01")))