from rest_framework.pagination import PageNumberPagination

class OrdersPagination(PageNumberPagination): # Classe de paginação para a view "Orders"
    page_query_param = "page"
    page_size_query_param = "page_size"
    page_size = 10 # Define o tamanho padrão da página
    max_page_size = 100 # Define o tamanho máximo da página