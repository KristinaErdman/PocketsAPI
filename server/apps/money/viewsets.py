from django.db.models import Q, Sum, DecimalField
from django.db.models.functions import Coalesce
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from .models import Category, Transaction, Widget
from .utils import Paginate
from .serializers import (CategorySerializer, CategoryListSerializer, CategorySumByTypeSerializer,
                          TransactionSerializer, TransactionListSerializer,
                          WidgetSerializer, WidgetListSerializer)
from .filtersets import DateFilterSet
from .permissions import IsOwnerOrStaff


class CategoryViewSet(viewsets.ModelViewSet):
    """
    при получении метода POST создает новую категорию,
    при получении метода GET выводит список всех категорий,
    по адресу /with_sum/ и методе GET выводит список всех категорий с суммой транзакций по ним,
    при получении метода DELETE И id удаляет категорию с указанным id
    """
    permission_classes = [IsOwnerOrStaff, ]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get_queryset(self):
        self.queryset = Category.objects.filter(owner=self.request.user)
        return self.queryset

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        super(CategoryViewSet, self).perform_create(serializer)

    @action(methods=['get', ], detail=False, url_path='summary')
    def get_sum_amount(self, request):
        """Получение списка всех категорий текущего авторизованного пользователя
        с суммой транзакций по каждой категории. Если указаны параметры start_date и(или) end_date,
        при подсчете учитываются только транзакции из указанного периода."""
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
    permission_classes = [IsOwnerOrStaff, ]
    serializer_class = TransactionSerializer
    filterset_class = DateFilterSet
    pagination_class = Paginate

    def get_queryset(self):
        self.queryset = Transaction.objects.filter(owner=self.request.user)
        return self.queryset

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        super(TransactionViewSet, self).perform_create(serializer)

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


class WidgetViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrStaff, ]
    serializer_class = WidgetSerializer

    def get_queryset(self):
        self.queryset = Widget.objects.filter(owner=self.request.user)
        return self.queryset

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        super(WidgetViewSet, self).perform_create(serializer)

    def list(self, request, *args, **kwargs):
        self.serializer_class = WidgetListSerializer
        return super(WidgetViewSet, self).list(request, *args, **kwargs)
