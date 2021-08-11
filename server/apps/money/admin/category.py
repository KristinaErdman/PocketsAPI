from django.contrib.admin import ModelAdmin, register, TabularInline
from ..models.category import Category
from .transaction import TransactionInline


class CategoryInline(TabularInline):
    model = Category
    fields = ('type', 'name')
    readonly_fields = ('type', 'name')
    extra = 0
    show_change_link = True
    can_delete = False


@register(Category)
class CategoryAdmin(ModelAdmin):
    fields = ('type', 'name')
    inlines = [TransactionInline, ]
