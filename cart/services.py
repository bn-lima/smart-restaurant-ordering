from .models import Cart, CartItem

def get_cart(device): # Pega um carrinho ativo ou cria um
    return Cart.objects.get_or_create(status="open", device=device)

def is_item_in_cart(cart, menu_item): # Verifica se o item existe no carrinho
    try:
        cart_item = CartItem.objects.get(cart=cart, menu_item=menu_item)
    except CartItem.DoesNotExist:
        return None
    return cart_item