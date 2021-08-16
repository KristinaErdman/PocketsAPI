from django_filters import FilterSet, DateFilter
from .models import Transaction


class DateFilterSet(FilterSet):
    """FilterSet для фильтрации временного промежутка"""
    start_date = DateFilter(field_name='date', lookup_expr='gte')
    end_date = DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = Transaction
        fields = ['start_date', 'end_date', ]
