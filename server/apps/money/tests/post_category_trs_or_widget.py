import datetime
from dateutil import tz
from datetime import timedelta
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from apps.users.models import CustomUser
from ..models import Category, Transaction, Widget
from ..serializers import TransactionSerializer, CategorySerializer, WidgetSerializer
from .factory_data import UserFactory, CategoryFactory, TransactionFactory, WidgetFactory


class PostCategoryTransactionWidgetWithValidToken(APITestCase):
    client = APIClient()

    def setUp(self):
        self.user_data = {'email': 'testuser@mail.ru', 'username': 'TestUser',
                          'password': 'password'}
        # регистрация
        register_url = reverse('sign_up')
        reg_response = self.client.post(register_url, data=self.user_data)

        # авторизация
        data_for_auth = {'email': self.user_data['email'], 'password': self.user_data['password']}
        login_url = reverse('sign_in')
        auth_response = self.client.post(login_url, data=data_for_auth)
        self.token = auth_response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {self.token}')

        self.user = CustomUser.objects.get(username=self.user_data['username'])
        self.category = CategoryFactory(type='i', owner=self.user)
        self.transaction = TransactionFactory(owner=self.user, category=self.category,
                                                amount='50_000', date='2021-07-18')

    def test_post_category(self):
        """добавление категории"""
        serializer_data = CategorySerializer({'type': 'e', 'name': 'одежда', }).data
        url = reverse('category-list')
        response = self.client.post(url, data=serializer_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_category = Category.objects.last()
        self.assertEqual(new_category.owner, self.user)

    def test_post_transaction(self):
        """добавление транзакции"""
        serializer_data = TransactionSerializer({'category': self.category, 'amount': 5_000,
                                                 'date': '2021-08-18'}).data
        url = reverse('transaction-list')
        response = self.client.post(url, data=serializer_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_widget(self):
        """добавление виджета"""
        serializer_data = WidgetSerializer({'category': self.category, 'limit': 5_000,
                                            'duration': timedelta(days=30),
                                            'condition': 'l',
                                            'color': '#064787'}).data
        url = reverse('widget-list')
        response = self.client.post(url, data=serializer_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class PostCategoryTransactionWidgetWithInvalidToken(APITestCase):
    client = APIClient()

    def setUp(self):
        self.user_data = {'email': 'testuser@mail.ru', 'username': 'TestUser',
                          'password': 'password'}
        # регистрация
        register_url = reverse('sign_up')
        reg_response = self.client.post(register_url, data=self.user_data)

        # авторизация
        data_for_auth = {'email': self.user_data['email'], 'password': self.user_data['password']}
        login_url = reverse('sign_in')
        auth_response = self.client.post(login_url, data=data_for_auth)
        self.token = auth_response.data["access"]+'abrakadabra'

        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {self.token}')

        self.user = CustomUser.objects.get(username=self.user_data['username'])
        self.category = CategoryFactory(type='i', owner=self.user)
        self.transaction = TransactionFactory(owner=self.user, category=self.category,
                                              amount='50_000', date='2021-07-18')

    def test_post_category(self):
        """добавление категории"""
        serializer_data = CategorySerializer({'type': 'e', 'name': 'одежда', }).data
        url = reverse('category-list')
        response = self.client.post(url, data=serializer_data)
        self.assertTrue(status.is_client_error(response.status_code))

    def test_post_transaction(self):
        """добавление транзакции"""
        serializer_data = TransactionSerializer({'category': self.category, 'amount': 5_000,
                                                 'date': '2021-08-18'}).data
        url = reverse('transaction-list')
        response = self.client.post(url, data=serializer_data)
        self.assertTrue(status.is_client_error(response.status_code))

    def test_post_widget(self):
        """добавление виджета"""
        serializer_data = WidgetSerializer({'category': self.category, 'limit': 5_000,
                                            'duration': timedelta(days=30), 'condition': 'l',
                                            'color': '#064787'}).data
        url = reverse('widget-list')
        response = self.client.post(url, data=serializer_data)
        self.assertTrue(status.is_client_error(response.status_code))
