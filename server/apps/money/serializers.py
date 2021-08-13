from django.db.models import Sum
from django.db.models.functions import Coalesce
from rest_framework.serializers import (Serializer, ModelSerializer,
                                        SerializerMethodField, DecimalField)
from .models import Category, Transaction


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('pk', 'type', 'name', 'owner', )


class CategoryListSerializer(ModelSerializer):
    sum_amount = SerializerMethodField()

    class Meta:
        model = Category
        fields = ('pk', 'type', 'name', 'owner', 'sum_amount', )

    def get_sum_amount(self, obj):
        res = obj.transactions.aggregate(sum=Coalesce(Sum('amount'), 0.0,
                                                      output_field=DecimalField()))
        return res['sum']


class CategorySumByTypeSerializer(Serializer):
    income = DecimalField(read_only=True, max_digits=12, decimal_places=2)
    expense = DecimalField(read_only=True, max_digits=12, decimal_places=2)


class TransactionSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('pk', 'owner', 'category', 'amount', 'date', )


class TransactionListSerializer(ModelSerializer):
    type = SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ('pk', 'owner', 'category', 'amount', 'date', 'type', )

    def get_type(self, obj):
        return obj.category.type
