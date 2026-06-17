import django_filters
from kitchen.models import Order    
class DeliveredOrdersFilter(django_filters.FilterSet): # classe para filtrar pedido por data de criação e data que foi entregue

    created_at = django_filters.DateTimeFilter( 
        field_name="created_at", # campo do model Order que será filtrado
        lookup_expr="gte" # pega registros a partir da data (maior ou igual)
    )

    delivered_at = django_filters.DateTimeFilter(
        field_name="delivered_at",
        lookup_expr="lte" # pega registros até a data (menor ou igual)
    )

    class Meta:
        model = Order
        fields = []

class PendingOrdersFilter(django_filters.FilterSet): # Classe para filtrar pedidos não entregues

    created_at = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="gte"
    )

    created_at_to = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="lte"
    )

    class Meta:
        model = Order
        fields = []