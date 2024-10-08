from rest_framework import pagination

class MenuItemsPagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'perpage'
    max_page_size = 50
    page_query_param = 'page'
    
class CategoryPagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'perpage'
    max_page_size = 20
    page_query_param = 'page'