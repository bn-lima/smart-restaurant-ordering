from .models import MenuItem
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.postgres.search import SearchQuery, SearchVector
from .serializers import MenuItemsSerializer 
from .pagination import MenuItemsPagination

class MenuItems(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MenuItemsSerializer
    queryset = MenuItem.objects.all()
    pagination_class = MenuItemsPagination

    def get_queryset(self):
        search_qp = self.request.query_params.get("search") # Pega o parâmetro de pesquisa enviado na URL

        queryset = self.queryset.filter(active=True)

        if search_qp:

            search_vector = SearchVector("category")  # Cria o vetor de busca baseado no campo category
            
            search_query = SearchQuery(search_qp) # Converte o texto pesquisado em uma SearchQuery

            return queryset.annotate(search=search_vector).filter(search=search_query) # Adiciona o campo de busca ao queryset e filtra os resultados
        
        return queryset