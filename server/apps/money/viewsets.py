from django.db.models import Q, F, Sum, DecimalField
from django.db.models.functions import Coalesce
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from .utils import Paginate
from .models import Category, Transaction
from .serializers import (CategorySerializer, CategoryListSerializer, CategorySumByTypeSerializer,
                          TransactionSerializer, TransactionListSerializer)
from .filtersets import DateFilterSet


class CategoryViewSet(viewsets.ModelViewSet):
    """
    при получении метода POST создает новую категорию,
    при получении метода GET выводит список всех категорий,
    по адресу /with_sum/ и методе GET выводит список всех категорий с суммой транзакций по ним,
    при получении метода DELETE И id удаляет категорию с указанным id
    """
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    @action(methods=['get', ], detail=False, url_path='summary')
    def get_sum_amount(self, request):
        fs = DateFilterSet(self.request.GET, request=self.request,
                           queryset=Transaction.objects.all())
        transactions = fs.qs  # отфильтрованные по дате транзакции
        transactions = transactions.values('category').annotate(
            pk=F('category'),
            type=F('category__type'),
            name=F('category__name'),
            owner=F('category__owner'),
            sum_amount=Coalesce(Sum('amount'), 0.0, output_field=DecimalField()),
        )  # отфильтрованные по дате транзакции

        ser = CategoryListSerializer(transactions, many=True)
        return Response(ser.data, status=HTTP_200_OK)


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
    filterset_class = DateFilterSet
    pagination_class = Paginate

    def list(self, request, *args, **kwargs):
        self.serializer_class = TransactionListSerializer
        return super(TransactionViewSet, self).list(request, *args, **kwargs)

    @action(methods=['get', ], detail=False, url_path='global')
    def get_sum_income_and_expense(self, request):
        sum_by_categories = self.filter_queryset(self.queryset)
        sum_by_categories = sum_by_categories.aggregate(
            income=Coalesce(Sum('amount', filter=Q(category__type='i')), 0,
                output_field=DecimalField()),
            expense=Coalesce(Sum('amount', filter=Q(category__type='e')), 0,
                output_field=DecimalField()),
        )
        ser = CategorySumByTypeSerializer(sum_by_categories)
        return Response(ser.data, status=HTTP_200_OK)

