from django.db.models import Q, Sum, DecimalField
from django.db.models.functions import Coalesce
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from .utils import Paginate
from .models import Category, Transaction
from .serializers import (CategorySerializer, CategoryListSerializer, CategorySumByTypeSerializer,
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

    @action(methods=['get', ], detail=False)
    def from_date_to_date(self, request):
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)

        if start_date is not None and end_date is None:
            q_by_date = Q(date__gte=start_date)

        if end_date is not None and start_date is None:
            q_by_date = Q(date__lte=end_date)

        if start_date is not None and end_date is not None:
            q_by_date = Q(date__range=(start_date, end_date))

        try:
            sum_by_categories = Transaction.objects.aggregate(
                income=Coalesce(Sum('amount', filter=q_by_date & Q(category__type='i')), 0,
                                output_field=DecimalField()),
                expense=Coalesce(Sum('amount', filter=q_by_date & Q(category__type='e')), 0,
                                 output_field=DecimalField()),
            )
            ser = CategorySumByTypeSerializer(sum_by_categories)
            response = Response(ser.data, status=HTTP_200_OK)
        except Exception:
            response = Response(status=HTTP_400_BAD_REQUEST)
        finally:
            return response
