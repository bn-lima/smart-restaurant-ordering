from django.contrib import admin
from .models import Device

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("username", "function", "login_attempts", "blocked_until", "is_blocked")
    search_fields = ("username", "function", "login_attempts")
    list_filter = ("is_blocked",)