from .models import Order
from django.utils import timezone

def create_order(cart): # Cria um pedido
    return Order.objects.create(
        cart=cart
    )

def get_order_by_id(id): # Pega um pedido com id específico
    try:
        order = Order.objects.get(id=id)
    except Order.DoesNotExist:
        return None
    return order

def deliver_order(order): # Marca pedido como entregue
    order.delivered = True
    order.delivered_at = timezone.now()
    return order.save()

def order_exists(cart): # Verifica se um pedido com um carrinho específico já existe
    try:
        order = Order.objects.get(cart=cart)
    except Order.DoesNotExist:
        return False
    return True