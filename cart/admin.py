from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    extra = 1
    model = CartItem
    fields = ("quantity", "menu_item", "get_subtotal")
    readonly_fields = ("get_subtotal",)
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("device", "created_at", "status", "get_total")
    search_fields = ("device__id", "created_at", "status")

    inlines = [CartItemInline]