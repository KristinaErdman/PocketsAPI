from django.db import models
from django.db.models import CASCADE, UniqueConstraint
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from apps.users.models import CustomUser


class Category(models.Model):
    """Модель категории транзакции"""
    TYPE = (
        ('i', 'доход'),  # income
        ('e', 'расход'),  # expense
    )
    type = models.CharField(max_length=1, choices=TYPE, default='e', verbose_name='Тип')
    name = models.CharField(max_length=30, default=_('Other'), verbose_name='Название')
    owner = models.ForeignKey(CustomUser, on_delete=CASCADE, related_name='categories',
                              verbose_name='Владелец')

    class Meta:
        constraints = (UniqueConstraint(fields=('name', 'owner'), name='unique_for_owner'), )
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Transaction(models.Model):
    """Модель транзакции"""
    owner = models.ForeignKey(CustomUser, on_delete=CASCADE, related_name='transactions',
                              verbose_name='Владелец')
    category = models.ForeignKey(Category, on_delete=CASCADE,  blank=True,
                                 null=True, related_name='transactions', verbose_name='Категория')
    amount = models.DecimalField(max_digits=10, decimal_places=2,
                                 validators=[MinValueValidator(0.1), ], verbose_name='Сумма')
    date = models.DateField(verbose_name='Дата операции')

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'

    def __str__(self):
        return f'{self.date}\t{self.category.name}\t{self.amount}'
