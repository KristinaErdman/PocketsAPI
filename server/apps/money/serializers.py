from django.db.models import Sum, DecimalField
from django.db.models.functions import Coalesce
from rest_framework import serializers
from .models import Category, Transaction
from .filtersets import DateFilterSet


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('pk', 'type', 'name', 'owner', )


class CategoryListSerializer(serializers.ModelSerializer):
    sum_amount = serializers.DecimalField(read_only=True, max_digits=12, decimal_places=2)

    class Meta:
        model = Category
        fields = ('pk', 'type', 'name', 'owner', 'sum_amount', )

    def to_representation(self, instance):
        request = self.context['request']
        fs = DateFilterSet(request.GET, request=request, queryset=instance.transactions.all())
        filtered_transactions = fs.qs  # отфильтрованные по дате транзакции
        sum = filtered_transactions.aggregate(
            amount=Coalesce(Sum('amount'), 0.0, output_field=DecimalField()),
        )
        instance.sum_amount = sum['amount']
        return super(CategoryListSerializer, self).to_representation(instance)


class CategorySumByTypeSerializer(serializers.Serializer):
    income = serializers.DecimalField(read_only=True, max_digits=12, decimal_places=2)
    expense = serializers.DecimalField(read_only=True, max_digits=12, decimal_places=2)


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('pk', 'owner', 'category', 'amount', 'date', )


class TransactionListSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ('pk', 'owner', 'category', 'amount', 'date', 'type', )

    def get_type(self, obj):
        return obj.category.type
