from django.contrib import admin
from .models import Device

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("username", "function", "point_terminal_id")
    search_fields = ("username", "function", "point_terminal_id")