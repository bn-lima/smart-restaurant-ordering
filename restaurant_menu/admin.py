from django.contrib import admin
from .models import MenuItem

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "ingredients", "price", "active", "category")
    search_fields = ("name", "description", "ingredients", "price", "category")
    list_filter = ("active",)