from rest_framework import serializers
from .models import Category, Transaction


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('pk', 'type', 'name', 'owner', )


class CategoryListSerializer(serializers.Serializer):
    category = serializers.IntegerField()
    pk = serializers.IntegerField()
    type = serializers.CharField()
    name = serializers.CharField()
    owner = serializers.IntegerField()
    sum_amount = serializers.DecimalField(read_only=True, max_digits=12, decimal_places=2)


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
