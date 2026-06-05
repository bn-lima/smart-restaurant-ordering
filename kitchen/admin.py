from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("cart", "delivered", "created_at", "delivered_at")
    search_fields = ("cart__id", "created_at", "delivered_at")
    list_filter = ("delivered",)