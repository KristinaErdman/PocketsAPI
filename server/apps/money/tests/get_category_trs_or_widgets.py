from datetime import timedelta
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from apps.users.models import CustomUser
from ..models import Category, Transaction, Widget
from ..serializers import (TransactionSerializer, TransactionListSerializer,
                           CategorySerializer,
                           WidgetSerializer, WidgetListSerializer)
from .factory_data import UserFactory, CategoryFactory, TransactionFactory, WidgetFactory


class GetCategoryTransactionWidgetFromUser(APITestCase):
    client = APIClient()

    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

        self.category_1 = CategoryFactory(type='i', owner=self.user)
        self.category_2 = CategoryFactory(type='i', owner=self.user)

        self.transaction_1 = TransactionFactory(owner=self.user, category=self.category_1,
                                                        amount='50_000', date='2021-07-18')
        self.transaction_2 = TransactionFactory(owner=self.user, category=self.category_1,
                                                        amount='50_000', date='2021-08-18')
        self.transaction_3 = TransactionFactory(owner=self.user, category=self.category_2,
                                                amount='3_000')
        self.transaction_4 = TransactionFactory(owner=self.user, category=self.category_2,
                                                amount='1_000')
        self.transaction_5 = TransactionFactory(owner=self.user, category=self.category_1,
                                                amount='50_000')

        self.widget_1 = WidgetFactory(owner=self.user, category=self.category_1, limit=3_000)
        self.widget_2 = WidgetFactory(owner=self.user, category=self.category_2, limit=20_000)

        self.other_user = UserFactory(username='OtherUser')
        self.category_other_user = CategoryFactory(type='i', owner=self.other_user)
        self.transaction_other_user = TransactionFactory(owner=self.other_user,
                                                         category=self.category_other_user,
                                                         amount='5_000',
                                                         date='2021-08-10')
        self.widget_other_user = WidgetFactory(owner=self.other_user,
                                               category=self.category_other_user, limit=3_000)

    def test_get_my_category(self):
        """получение своей категории"""
        url = reverse('category-detail', kwargs={'pk': self.category_1.pk})
        response = self.client.get(url)

        users_category = Category.objects.get(pk=self.category_1.pk)
        serializer_data = CategorySerializer(users_category).data

        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data, serializer_data)

    def test_get_other_category(self):
        """попытка получения чужой категории"""
        url = reverse('category-detail', kwargs={'pk': self.category_other_user.pk})
        response = self.client.get(url)
        self.assertTrue(status.is_client_error(response.status_code))

    def test_get_my_transaction(self):
        """получение своей транзакции"""
        url = reverse('transaction-detail', kwargs={'pk': self.transaction_1.pk})
        response = self.client.get(url)

        users_transaction = Transaction.objects.get(pk=self.transaction_1.pk)
        serializer_data = TransactionSerializer(users_transaction).data

        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data, serializer_data)

    def test_get_other_transaction(self):
        """попытка получения чужой транзакции"""
        url = reverse('transaction-detail', kwargs={'pk': self.transaction_other_user.pk})
        response = self.client.get(url)
        self.assertTrue(status.is_client_error(response.status_code))

    def test_get_my_widget(self):
        """получение своего виджета"""
        url = reverse('widget-detail', kwargs={'pk': self.widget_1.pk})
        response = self.client.get(url)

        users_widget = Widget.objects.get(pk=self.widget_1.pk)
        serializer_data = WidgetSerializer(users_widget).data

        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data, serializer_data)

    def test_get_other_widget(self):
        """попытка получения чужого виджета"""
        url = reverse('widget-detail', kwargs={'pk': self.widget_other_user.pk})
        response = self.client.get(url)
        self.assertTrue(status.is_client_error(response.status_code))

    def test_get_all_categories(self):
        """при запросе списка категорий получаем только свои"""
        url = reverse('category-list')
        response = self.client.get(url)
        serializer_data = CategorySerializer(Category.objects.filter(owner=self.user),
                                             many=True).data
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data, serializer_data)

    def test_get_all_transactions(self):
        """при запросе списка транзакций получаем только свои"""
        url = reverse('transaction-list')
        response = self.client.get(url)
        result = response.data['results']
        serializer_data = TransactionListSerializer(Transaction.objects.filter(owner=self.user),
                                                    many=True).data
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(result, serializer_data)

    def test_get_all_widgets(self):
        """при запросе списка виджетов получаем только свои"""
        url = reverse('widget-list')
        response = self.client.get(url)
        serializer_data = WidgetListSerializer(Widget.objects.filter(owner=self.user),
                                           many=True).data
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data, serializer_data)

    def tearDown(self):
        self.client.logout()


class GetCategoryTransactionWidgetFromAnonym(APITestCase):
    client = APIClient()

    def setUp(self):
        self.user = UserFactory()

        self.category_1 = CategoryFactory(type='i', owner=self.user)
        self.category_2 = CategoryFactory(type='i', owner=self.user)

        self.transaction_1 = TransactionFactory(owner=self.user, category=self.category_1,
                                                        amount='50_000', date='2021-07-18')
        self.transaction_2 = TransactionFactory(owner=self.user, category=self.category_1,
                                                        amount='50_000', date='2021-08-18')
        self.transaction_3 = TransactionFactory(owner=self.user, category=self.category_2,
                                                amount='3_000')
        self.transaction_4 = TransactionFactory(owner=self.user, category=self.category_2,
                                                amount='1_000')
        self.transaction_5 = TransactionFactory(owner=self.user, category=self.category_1,
                                                amount='50_000')

        self.widget_1 = WidgetFactory(owner=self.user, category=self.category_1, limit=3_000)
        self.widget_2 = WidgetFactory(owner=self.user, category=self.category_2, limit=20_000)

    def test_get_category(self):
        """попытка получения одной категории"""
        url = reverse('category-detail', kwargs={'pk': self.category_1.pk})
        response = self.client.get(url)
        self.assertTrue(status.is_client_error(response.status_code))

    def test_get_all_categories(self):
        """попытка получения списка всех категорий"""
        url = reverse('category-list')
        response = self.client.get(url)
        self.assertTrue(status.is_client_error(response.status_code))

    def test_get_transaction(self):
        """попытка получения одной транзакции"""
        url = reverse('transaction-detail', kwargs={'pk': self.transaction_1.pk})
        response = self.client.get(url)
        self.assertTrue(status.is_client_error(response.status_code))

    def test_get_all_transactions(self):
        """попытка получения списка всех транзакций"""
        url = reverse('transaction-list')
        response = self.client.get(url)
        self.assertTrue(status.is_client_error(response.status_code))

    def test_get_widget(self):
        """попытка получения одного виджета"""
        url = reverse('widget-detail', kwargs={'pk': self.widget_1.pk})
        response = self.client.get(url)
        self.assertTrue(status.is_client_error(response.status_code))

    def test_get_all_widgets(self):
        """попытка получения списка всех виджетов"""
        url = reverse('widget-list')
        response = self.client.get(url)
        self.assertTrue(status.is_client_error(response.status_code))
