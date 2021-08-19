import datetime
from datetime import timedelta
import factory
from apps.users.models import CustomUser
from ..models import Category, Transaction, Widget


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    username = 'TestUser'
    email = factory.LazyAttribute(lambda obj: '%s@mail.ru' % obj.username)
    password = 'password'


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    type = None
    name = factory.Sequence(lambda n: 'категория_%d' % n)
    owner = None


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transaction

    owner = None
    category = None
    amount = None
    date = datetime.date(year=2021, month=8, day=18)


class WidgetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Widget

    owner = None
    category = None
    limit = None
    duration = timedelta(days=30)
    condition = 'l'
    color = '#627aac'
    created_date = datetime.date(year=2021, month=8, day=18)
    expiry_date = factory.LazyAttribute(lambda obj: obj.created_date + obj.duration)
