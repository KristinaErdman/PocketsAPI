from rest_framework.pagination import PageNumberPagination


class Paginate(PageNumberPagination):
    page_size = 10
