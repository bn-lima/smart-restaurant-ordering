from django.db import models
from cart.models import Cart

class Order(models.Model):
   cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
   delivered = models.BooleanField(default=False)
   created_at = models.DateTimeField(auto_now_add=True)
   delivered_at = models.DateTimeField(blank=True, null=True)

   def __str__(self):
      return f"Cart: #{self.cart} - {self.created_at}"