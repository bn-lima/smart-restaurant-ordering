from django.db import models
from .constants import CartStatusChoices
from devices.models import Device
from restaurant_menu.models import MenuItem
from django.contrib import admin
class Cart(models.Model): # Modelo do carrinho
    device = models.ForeignKey(Device, related_name="carts", on_delete=models.CASCADE) # Dispositivo que criou o carrinho
    created_at = models.DateTimeField(auto_now_add=True) # Data e hora de criação do carrinho
    status = models.CharField(max_length=9, choices=CartStatusChoices.choices(), default=CartStatusChoices.OPEN.value) # Status do carrinho

    @admin.display(description="Total")
    def get_total(self): # Retotna total do carrinho
        return sum((item.get_subtotal()) for item in self.items.all())

    def __str__(self):
        return f"{self.device.username} - {self.created_at}"
class CartItem(models.Model): # Modelo do item do carrinho
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE) # Carrinho relacionado
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE) # Item do carrinho
    quantity = models.PositiveIntegerField() # Quantidade do item
    
    @admin.display(description="Subtotal")
    def get_subtotal(self): # Retorna subtotal do item
        return (self.menu_item.item_price * self.quantity)
    
    def __str__(self):
        return f"{self.menu_item.item_name} - {self.quantity}"