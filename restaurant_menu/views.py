from .models import MenuItem
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import permissions
from django.contrib.postgres.search import SearchQuery, SearchVector
from .serializers import MenuItemsSerializer, MenuItemDetailSerializer
from .pagination import MenuItemsPagination
from rest_framework.response import Response

class MenuItems(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MenuItemsSerializer
    queryset = MenuItem.objects.all()
    pagination_class = MenuItemsPagination

    def list(self, request, *args, **kwargs):
        if request.user.function == "kitchen":
            return Response({"detail": "You do not have permission to access this endpoint"}, status=403)
        return super().list(request, *args, **kwargs)
        
    def get_queryset(self):
        search_qp = self.request.query_params.get("search") # Pega o parâmetro de pesquisa enviado na URL

        queryset = self.queryset.filter(active=True)

        if search_qp:

            search_vector = SearchVector("item_category")  # Cria o vetor de busca baseado no campo category
            
            search_query = SearchQuery(search_qp) # Converte o texto pesquisado em uma SearchQuery

            return queryset.annotate(search=search_vector).filter(search=search_query) # Adiciona o campo de busca ao queryset e filtra os resultados
        
        return queryset
    
class MenuItemDetail(RetrieveAPIView): # View responsável por mostrar os detalhes de um item específico no menu
    permission_classes =  [permissions.IsAuthenticated]
    queryset = MenuItem.objects.filter(active=True)
    serializer_class = MenuItemDetailSerializer