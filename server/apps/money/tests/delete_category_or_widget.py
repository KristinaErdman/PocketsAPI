from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from ..models import Category, Widget
from .factory_data import UserFactory, CategoryFactory, TransactionFactory, WidgetFactory


class DeleteCategoryOrWidgetFromUser(APITestCase):
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

    def test_delete_my_category(self):
        """удаление своей категории"""
        count_categories = Category.objects.count()
        url = reverse('category-detail', kwargs={'pk': self.category_2.pk})
        response = self.client.delete(url)
        self.assertTrue(status.is_success(response.status_code))
        self.assertTrue(Category.objects.count() is count_categories - 1)

    def test_delete_other_category(self):
        """попытка удаления чужой категории"""
        count_categories = Category.objects.count()
        url = reverse('category-detail', kwargs={'pk': self.category_other_user.pk})
        response = self.client.delete(url)
        self.assertTrue(status.is_client_error(response.status_code))
        self.assertTrue(Category.objects.count() is count_categories)

    def test_delete_my_widget(self):
        """удаление своего виджета"""
        count_widgets = Widget.objects.count()
        url = reverse('widget-detail', kwargs={'pk': self.widget_1.pk})
        response = self.client.delete(url)
        self.assertTrue(status.is_success(response.status_code))
        self.assertTrue(Widget.objects.count() is count_widgets - 1)

    def test_delete_other_widget(self):
        """попытка удаления чужого виджета"""
        count_widgets = Widget.objects.count()
        url = reverse('widget-detail', kwargs={'pk': self.widget_other_user.pk})
        response = self.client.delete(url)
        self.assertTrue(status.is_client_error(response.status_code))
        self.assertTrue(Widget.objects.count() is count_widgets)

    def tearDown(self):
        self.client.logout()


class DeleteCategoryOrWidgetFromAnonym(APITestCase):
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

    def test_delete_category(self):
        count_categories = Category.objects.count()
        url = reverse('category-detail', kwargs={'pk': Category.objects.first().pk})
        response = self.client.delete(url)
        self.assertTrue(status.is_client_error(response.status_code))
        self.assertTrue(Category.objects.count() is count_categories)

    def test_delete_widget(self):
        count_widgets = Widget.objects.count()
        url = reverse('widget-detail', kwargs={'pk': Widget.objects.first().pk})
        response = self.client.delete(url)
        self.assertTrue(status.is_client_error(response.status_code))
        self.assertTrue(Widget.objects.count() is count_widgets)
