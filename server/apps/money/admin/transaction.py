from django.contrib.admin import TabularInline
from ..models.transaction import Transaction


class TransactionInline(TabularInline):
    model = Transaction
    fk_name = 'category'
    fields = ('date', 'amount')
    ordering = ('-date', )
    extra = 0
