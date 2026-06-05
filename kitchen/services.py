from .models import Order

def create_order(cart):
    return Order.objects.create(
        cart=cart
    )