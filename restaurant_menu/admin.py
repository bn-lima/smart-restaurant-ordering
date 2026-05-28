from django.contrib import admin
from .models import MenuItem

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("item_name", "item_ingredients", "item_price", "active", "item_category")
    search_fields = ("item_name", "item_description", "item_ingredients", "item_price", "category")
    list_filter = ("active",)