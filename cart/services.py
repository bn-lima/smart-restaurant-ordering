from .models import Cart, CartItem

def get_cart(device): # Pega um carrinho ativo ou cria um
    return Cart.objects.get_or_create(status="open", device=device)

def is_item_in_cart(cart, menu_item): # Verifica se o item existe no carrinho
    try:
        cart_item = CartItem.objects.get(cart=cart, menu_item=menu_item)
    except CartItem.DoesNotExist:
        return None
    return cart_item

def cancel_cart(cart): # Cancela o carrinho
    cart.status = "canceled"
    return cart.save()

def remove_inactive_cart_items(cart): # Retorna FALSO se não encontrar nenhum item inativo no carrinho
    deleted_count, _ = cart.items.filter(menu_item__active=False).delete()
    return deleted_count > 0

def get_cart_by_id(id): # Pega carrinho por id
    try:
        cart = Cart.objects.get(id=id)
    except Cart.DoesNotExist:
        return None
    return cart