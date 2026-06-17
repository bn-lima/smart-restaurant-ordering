from rest_framework import serializers
from devices.models import Device
from restaurant_menu.models import MenuItem
from devices.validators import PASSWORD_VALIDATOR
from kitchen.models import Order
from cart.models import Cart, CartItem

class DeviceListSerializer(serializers.ModelSerializer): # Serializer responsável por listar todos os dispositivos
    device_id = serializers.SerializerMethodField() # Id do dispositivo

    class Meta:
        model = Device()
        fields = ("username", "function", "device_id")

    def get_device_id(self, obj): # Retorna o id do dispositivo
        return int(obj.id)  
class UpdateDeviceSerializer(serializers.ModelSerializer): # Serializer responsável por atualizar dados do dispositivo
    confirmation_password = serializers.CharField(required=True, max_length=128, write_only=True) # Senha de confirmação do super usuário
    confirm_password = serializers.CharField(required=False, max_length=128, write_only=True, validators=[PASSWORD_VALIDATOR]) # Confirmar nova senha
    class Meta:
        model = Device
        fields = ("username", "password", "function", "confirmation_password", "confirm_password")

        extra_kwargs = { # Adiciona parâmetros extras pros campos username, password e function
            "username": {"required": False, "validators": []},
            "password": {"required": False, "validators": [PASSWORD_VALIDATOR]},
            "function": {"required": False}
        }

    def validate(self, data):
        authenticated_device = self.context.get("authenticated_device") # Super usuário

        new_password = data.get("password") # Nova senha a ser setada
        confirm_password = data.get("confirm_password") # Confirmar nova senha
       
        if not authenticated_device.check_password(data["confirmation_password"]): # Valida se a senha do super usuário digitada está correta
            raise serializers.ValidationError("Invalid password")   
        
        if new_password or confirm_password:

            if not new_password:
                raise serializers.ValidationError("password is required")

            if not confirm_password: # Valida se confirm_new_password foi enviado
                raise serializers.ValidationError("Confirm password is required")
            
            if self.instance.check_password(new_password): # Valida se a nova senha é igual a senha atual
                raise serializers.ValidationError("The new password cannot be the same as the current password")

            if new_password != confirm_password: # Valida se a nova senha e confirmar senha são iguais
                raise serializers.ValidationError("Passwords do not match")
        
        return data
    
    def save(self, **kwargs):
        self.validated_data.pop("confirm_password", None) # Remove o campo de confirmação de nova senha dos dados validados
        password = self.validated_data.pop("password", None) # Remove password dos dados validados para definir a nova senha de forma segura

        if password:
            self.instance.set_password(password) # Define a nova senha de forma segura
 
        return super().save(**kwargs)
    
class CreateDeviceSerializer(serializers.ModelSerializer): # Serializer responsável por criar um dispositivo via admin
    confirmation_password = serializers.CharField(max_length=128, write_only=True) # Senha de confirmação do super usuário
    confirm_password = serializers.CharField(max_length=128, validators=[PASSWORD_VALIDATOR], write_only=True) # Confirmar senha do dispositivo
    class Meta:
        model = Device
        fields = ("username", "password", "confirm_password", "confirmation_password","function")

    def validate(self, data):
        super_user = self.context.get("super_user") # Super usuário responsável pela criação do dispositivo

        if not super_user.check_password(data.get("confirmation_password")): # Verifica se a senha de confirmação do admin está correta
            raise serializers.ValidationError("Invalid confirmation password")
        
        if data.get("password") != data.get("confirm_password"): # Valida se as senhas batem
            raise serializers.ValidationError("Passwords do not match")
        
        return data
    
    def create(self, validated_data):
        password = validated_data.pop("password") # Remove password dos dados validados para setar no dispositivo de forma segura
        # Remove campos que não estão presentes no modelo Device
        validated_data.pop("confirm_password")
        validated_data.pop("confirmation_password")

        device = Device(**validated_data) # Cria uma instância de device
        device.set_password(password) # Define password de forma segura
        device.save()

        return device
class UpdateMenuItemSerializer(serializers.ModelSerializer): # Serializer responsável por atualizar dados de um item do menu
    confirmation_password = serializers.CharField(max_length=128, required=True, write_only=True)
    class Meta:
        model = MenuItem
        fields = '__all__'

        extra_kwargs = { # Torna todos os campos do modelo não obrigatórios
            "item_name": {"required":False},
            "item_description": {"required":False},
            "item_ingredients": {"required":False},
            "item_price": {"required":False},
            "active": {"required":False},
            "item_category": {"required":False},
            "item_image": {"required":False}
        }

    def validate(self, data):
        super_user = self.context.get("super_user") # Pega admin via context

        if not super_user.check_password(data.get("confirmation_password")): # Verifica se a senha de confirmação está correta
            raise serializers.ValidationError("Invalid confirmation password")
        
        return data
    
    def save(self, **kwargs):
        self.validated_data.pop("confirmation_password") # Remove a senha de confirmação dos dados validados, pois não existe no modelo
        return super().save(**kwargs)
    
class ConfirmationPasswordSerializier(serializers.Serializer): # Serializer responsável por validar senha de confirmação
    confirmation_password = serializers.CharField(required=True, max_length=128, write_only=True)

    def validate(self, data):
        super_user = self.context.get("super_user")

        if not super_user.check_password(data.get("confirmation_password")):
            raise serializers.ValidationError("Invalid confirmation password")
        
        return data
    
class AdminOrdersListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'

class AdminCartItemsDetailSerializer(serializers.ModelSerializer): # Mostra os itens de um carrinho
    menu_item_name = serializers.SerializerMethodField()
    menu_item_unit_price = serializers.SerializerMethodField()
    menu_item_subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ("menu_item", "menu_item_name", "quantity", "menu_item_unit_price", "menu_item_subtotal")

    def get_menu_item_name(self, obj):
        return obj.menu_item.item_name
    
    def get_menu_item_subtotal(self, obj):
        return obj.get_subtotal()
    
    def get_menu_item_unit_price(self, obj):
        return obj.menu_item.item_price

class AdminCartDetailSerializer(serializers.ModelSerializer): # Mostra o carrinho do pedido
    items = AdminCartItemsDetailSerializer(many=True)

    class Meta:
        model = Cart
        fields = ("created_at", "status", "items")

class AdminOrderDetailSerializer(serializers.ModelSerializer): # Serializer responsável por mostrar os detalhes de um pedido específico
    cart = AdminCartDetailSerializer() # Carrinho do pedido
    order_id = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ("order_id", "delivered", "created_at", "delivered_at", "cart")

    def get_order_id(self, obj):
        return int(obj.id)