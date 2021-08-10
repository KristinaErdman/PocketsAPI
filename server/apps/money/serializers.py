from django.db.models import Sum
from rest_framework.serializers import ModelSerializer, SerializerMethodField
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
        res = obj.transactions.aggregate(sum=Sum('amount'))
        return res.get('sum', 0) if res.get('sum', 0) is not None else 0


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
