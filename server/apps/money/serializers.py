from django.db.models import Q, Sum, DecimalField
from django.db import models
from django.db.models.functions import Coalesce
from rest_framework import serializers
from .models import Category, Transaction, Widget
from .filtersets import DateFilterSet


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('pk', 'type', 'name', )


class CategoryListSerializer(serializers.ModelSerializer):
    sum_amount = serializers.DecimalField(read_only=True, max_digits=12, decimal_places=2)

    class Meta:
        model = Category
        fields = ('pk', 'type', 'name', 'sum_amount', )

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
        fields = ('pk', 'category', 'amount', 'date', )


class TransactionListSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ('pk', 'category', 'amount', 'date', 'type', )

    def get_type(self, obj):
        return obj.category.type


class WidgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Widget
        fields = ('pk', 'category', 'limit', 'duration', 'condition', 'color',
                  'created_date', 'expiry_date',)
        read_only_fields = ('expiry_date',)



class WidgetListSerializer(serializers.ModelSerializer):
    current_sum = serializers.SerializerMethodField()

    class Meta:
        model = Widget
        fields = ('pk', 'category', 'limit', 'duration', 'condition', 'color',
                  'created_date', 'expiry_date', 'current_sum', )
        read_only_fields = ('expiry_date', 'current_sum',)

    def get_current_sum(self, obj):
        # print(obj.expiry_date)
        q_by_date = models.Q(date__range=(obj.created_date, obj.expiry_date))
        q_by_category = models.Q(category=obj.category)
        transactions = Transaction.objects.aggregate(
            sum=Coalesce(models.Sum('amount', filter=q_by_category & q_by_date), 0.0,
                         output_field=models.DecimalField())
        )
        return transactions['sum']
