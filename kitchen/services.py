from .models import Order

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
    return order.save()