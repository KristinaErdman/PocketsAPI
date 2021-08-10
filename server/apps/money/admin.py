from django.contrib.admin import ModelAdmin, register, TabularInline
from .models import Category, Transaction


class CategoryInline(TabularInline):
    model = Category
    fields = ('type', 'name')
    readonly_fields = ('type', 'name')
    extra = 0
    show_change_link = True
    can_delete = False


class TransactionInline(TabularInline):
    model = Transaction
    fk_name = 'category'
    fields = ('date', 'amount')
    ordering = ('-date', )
    extra = 0


@register(Category)
class CategoryAdmin(ModelAdmin):
    fields = ('type', 'name')
    inlines = [TransactionInline, ]
