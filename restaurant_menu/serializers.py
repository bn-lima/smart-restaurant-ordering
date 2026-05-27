from rest_framework import serializers
from .models import MenuItem

class MenuItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = MenuItem
        exclude = ("active",)