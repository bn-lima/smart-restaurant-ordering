from rest_framework import serializers
from .models import MenuItem
class MenuItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        exclude = ("active",)

class CreateMenuItemSerializer(serializers.ModelSerializer): # Serializer responsável por criar um novo item no menu
    class Meta:
        model = MenuItem
        fields = '__all__'