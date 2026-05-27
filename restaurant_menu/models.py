from django.db import models
from .constants import MenuItemCategoryChoices

class MenuItem(models.Model):
    name = models.CharField(max_length=200) # Nome do item
    description = models.CharField(max_length=500) # descrição do item
    ingredients = models.TextField() # Ingredientes do item
    price = models.DecimalField(max_digits=5,decimal_places=2) # Preço do item
    active = models.BooleanField(default=False) # Define se o item está ativo ou não
    category = models.CharField(choices=MenuItemCategoryChoices.choices()) # Categoria do item
    image = models.ImageField(default="restaurant_menu/default.png", upload_to="restaurant/menu")

    def __str__(self):
        return f"{self.name} - {self.price}"