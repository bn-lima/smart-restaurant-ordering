from .models import Order

def create_order(cart):
    return Order.objects.create(
        cart=cart
    )

def get_order_by_id(id):
    try:
        order = Order.objects.get(id=id)
    except Order.DoesNotExist:
        return None
    return order

def deliver_order(order):
    order.delivered = True
    return order.save()