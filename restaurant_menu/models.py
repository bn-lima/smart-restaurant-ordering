from django.db import models
from .constants import MenuItemCategoryChoices

class MenuItem(models.Model):
    item_name = models.CharField(max_length=200) # Nome do item
    item_description = models.CharField(max_length=1000) # descrição do item
    item_ingredients = models.TextField(max_length=1000) # Ingredientes do item
    item_price = models.DecimalField(max_digits=5,decimal_places=2) # Preço do item
    active = models.BooleanField(default=False) # Define se o item está ativo ou não
    item_category = models.CharField(choices=MenuItemCategoryChoices.choices()) # Categoria do item
    item_image = models.ImageField(default="restaurant_menu/default.png", upload_to="restaurant/menu") # Categoria do item

    def __str__(self):
        return f"{self.name} - {self.price}"