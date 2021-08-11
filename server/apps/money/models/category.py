from django.db import models
from django.db.models import CASCADE, UniqueConstraint
from django.utils.translation import gettext_lazy as _
import apps.users.models


class Category(models.Model):
    """Модель категории транзакции"""
    TYPE = (
        ('i', 'доход'),  # income
        ('e', 'расход'),  # expense
    )
    type = models.CharField(max_length=1, choices=TYPE, verbose_name='Тип')
    name = models.CharField(max_length=30, default=_('Other'), verbose_name='Название')
    owner = models.ForeignKey(to=apps.users.models.CustomUser, on_delete=CASCADE, related_name='categories',
                              verbose_name='Владелец')

    class Meta:
        constraints = (UniqueConstraint(fields=('name', 'owner'), name='unique_for_owner'), )
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name
