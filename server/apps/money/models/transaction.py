from django.db import models
from django.db.models import CASCADE
from django.core.validators import MinValueValidator


class Transaction(models.Model):
    """Модель транзакции"""
    owner = models.ForeignKey(to='users.CustomUser', on_delete=CASCADE, related_name='transactions',
                              verbose_name='Владелец')
    category = models.ForeignKey(to='money.Category', on_delete=CASCADE,  blank=True,
                                 null=True, related_name='transactions', verbose_name='Категория')
    amount = models.DecimalField(max_digits=10, decimal_places=2,
                                 validators=[MinValueValidator(0.1), ], verbose_name='Сумма')
    date = models.DateField(verbose_name='Дата операции')

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'

    def __str__(self):
        return f'{self.date}\t{self.category.name}\t{self.amount}'
