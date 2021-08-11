from rest_framework import viewsets
from rest_framework.decorators import action
from .utils import Paginate
from .models import Category, Transaction
from .serializers import (CategorySerializer, CategoryListSerializer,
                          TransactionSerializer, TransactionListSerializer)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    при получении метода POST создает новую категорию,
    при получении метода GET выводит список всех категорий,
    по адресу /with_sum/ и методе GET выводит список всех категорий с суммой транзакций по ним,
    при получении метода DELETE И id удаляет категорию с указанным id
    """
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    @action(methods=['get', ], detail=False, url_path='with_sum')
    def get_sum_amount(self, request):
        self.serializer_class = CategoryListSerializer
        return self.list(request)


class TransactionViewSet(viewsets.ModelViewSet):
    """
        при получении метода POST создает новую транзакцию,
        при получении метода GET выводит список всех транзакций с указанием типа категории к которой
            они относятся,
        при получении метода DELETE И id удаляет транзакцию с указанным id,
        при получении метода PATCH И id обновляет транзакцию с указанным id,
    """
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    pagination_class = Paginate

    def list(self, request, *args, **kwargs):
        self.serializer_class = TransactionListSerializer
        return super(TransactionViewSet, self).list(request, *args, **kwargs)
