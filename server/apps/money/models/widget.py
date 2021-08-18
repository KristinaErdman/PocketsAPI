from datetime import timedelta
from django.db import models
from django.db.models import CASCADE
from django.core.validators import MinValueValidator, RegexValidator


class Widget(models.Model):
    """Модель виджета"""
    DURATION = (
        (timedelta(hours=24), 'day'),  # day
        (timedelta(weeks=1), 'week'),  # week
        (timedelta(days=30), 'month'),  # month
    )
    CONDITION = (
        ('m', 'больше'),  # more
        ('l', 'меньше'),  # less
    )
    owner = models.ForeignKey(to='users.CustomUser', on_delete=CASCADE, related_name='widgets',
                              verbose_name='Владелец')
    category = models.OneToOneField(to='money.Category', on_delete=CASCADE,
                                    verbose_name='Категория')
    limit = models.DecimalField(max_digits=10, decimal_places=2,
                                validators=[MinValueValidator(0.1), ],
                                verbose_name='Лимит суммы, которую можно потратить')
    duration = models.DurationField(choices=DURATION, verbose_name='Срок действия')
    condition = models.CharField(max_length=1, choices=CONDITION,
                                 verbose_name='Критерий (больше, меньше)')
    color = models.CharField(max_length=7, validators=[RegexValidator(r'#[a-f\d]{6}'), ],
                             default='#FF0000', verbose_name='Цвет(hex)')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    expiry_date = models.DateTimeField(verbose_name='Дата окончания цели')

    class Meta:
        verbose_name = 'Виджет'
        verbose_name_plural = 'Виджеты'

    def __str__(self):
        return f'тратить на {self.category} {self.condition} {self.limit} рублей'

    def save(self, *args, **kwargs):
        super(Widget, self).save(*args, **kwargs)
        self.expiry_date = self.created_date + self.duration
        super(Widget, self).save(update_fields=['expiry_date', ])
