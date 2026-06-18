from rest_framework import serializers
from .models import MenuItem

class MenuItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        exclude = ("active", "item_description", "item_ingredients")

class MenuItemDetailSerializer(serializers.ModelSerializer): # Serializer responsável por mostrar os detalhes de um item específico no menu
    class Meta:
        model = MenuItem
        exclude = ("active",)