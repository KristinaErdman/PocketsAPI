from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from apps.users.models import CustomUser
from ..models import Category, Transaction
from ..serializers import TransactionSerializer


class UpdateOrDeleteTransactionFromUser(APITestCase):
    client = APIClient()

    def setUp(self):
        self.user = CustomUser.objects.create_user(username='TestUser',
                                                   email='testuser@mail.ru',
                                                   password='password')
        self.client.force_authenticate(user=self.user)

        self.category_1 = Category.objects.create(type='i', name='зар.плата', owner=self.user)
        self.category_2 = Category.objects.create(type='e', name='жкс', owner=self.user)

        self.transaction_1 = Transaction.objects.create(owner=self.user, category=self.category_1,
                                                        amount='50_000', date='2021-07-18')
        self.transaction_2 = Transaction.objects.create(owner=self.user, category=self.category_1,
                                                        amount='50_000', date='2021-08-18')
        self.transaction_1 = Transaction.objects.create(owner=self.user, category=self.category_1,
                                                        amount='50_000', date='2021-07-18')
        self.transaction_3 = Transaction.objects.create(owner=self.user, category=self.category_2,
                                                        amount='3_000', date='2021-07-10')
        self.transaction_4 = Transaction.objects.create(owner=self.user, category=self.category_2,
                                                        amount='1_000', date='2021-07-10')

        self.other_user = CustomUser.objects.create_user(username='OtherUser',
                                                    email='otheruser@mail.ru',
                                                    password='password')
        self.category_other_user = Category.objects.create(type='e', name='питание',
                                                           owner=self.other_user)
        self.transaction_other_user = Transaction.objects.create(owner=self.other_user,
                                                                 category=self.category_other_user,
                                                                 amount='5_000',
                                                                 date='2021-08-10')

    def test_put_my_transaction(self):
        """полное обновление своей транзакции"""
        old_transaction = Transaction.objects.filter(owner=self.user).first()
        serializer = TransactionSerializer({'pk': Transaction.objects.count()+1,
                                            'category': Category.objects.filter(
                                                owner=self.user).first(),
                                            'amount': 1_500, 'date': '2021-08-15'})
        url = reverse('transaction-detail', kwargs={'pk': old_transaction.pk})
        response = self.client.put(url, data=serializer.data)
        self.assertTrue(status.is_success(response.status_code))
        new_transaction = Transaction.objects.filter(owner=self.user).first()
        self.assertTrue(old_transaction is not new_transaction)

    def test_put_other_transaction(self):
        """попытка полного обновления чужой транзакции"""
        old_transaction = Transaction.objects.filter(owner=self.other_user).first()
        serializer = TransactionSerializer({'pk': Transaction.objects.count() + 1,
                                            'category': Category.objects.filter(
                                                owner=self.other_user).first(),
                                            'amount': 1_500, 'date': '2021-08-15'})
        url = reverse('transaction-detail', kwargs={'pk': old_transaction.pk})
        response = self.client.put(url, data=serializer.data)
        self.assertTrue(status.is_client_error(response.status_code))
        new_transaction = Transaction.objects.filter(owner=self.other_user).first()
        self.assertEqual(old_transaction, new_transaction)

    def test_patch_my_transaction(self):
        """частичное обновление своей транзакции"""
        old_transaction = Transaction.objects.filter(owner=self.user).first()
        serializer = TransactionSerializer(old_transaction, data={'amount': 1500, }, partial=True)
        url = reverse('transaction-detail', kwargs={'pk': old_transaction.pk})
        response = self.client.patch(url, data=serializer.initial_data)
        self.assertTrue(status.is_success(response.status_code))
        new_transaction = Transaction.objects.filter(owner=self.user).first()
        self.assertTrue(old_transaction is not new_transaction)
        self.assertEqual(old_transaction.pk, new_transaction.pk)

    def test_patch_other_transaction(self):
        """попытка частичного обновления чужой транзакции"""
        old_transaction = Transaction.objects.filter(owner=self.other_user).first()
        serializer = TransactionSerializer(old_transaction, data={'amount': 1500, }, partial=True)
        url = reverse('transaction-detail', kwargs={'pk': old_transaction.pk})
        response = self.client.patch(url, data=serializer.initial_data)
        self.assertTrue(status.is_client_error(response.status_code))
        new_transaction = Transaction.objects.filter(owner=self.other_user).first()
        self.assertEqual(old_transaction, new_transaction)
        self.assertEqual(old_transaction.pk, new_transaction.pk)

    def test_delete_my_transaction(self):
        """удаление своей транзакции"""
        count_transactions = Transaction.objects.count()
        url = reverse('transaction-detail', kwargs={'pk': self.transaction_1.pk})
        response = self.client.delete(url)
        self.assertTrue(status.is_success(response.status_code))
        self.assertTrue(Transaction.objects.count() is count_transactions - 1)

    def test_delete_other_transaction(self):
        """попытка удаления чужой транзакции"""
        count_transactions = Transaction.objects.count()
        url = reverse('transaction-detail', kwargs={'pk': self.transaction_other_user.pk})
        response = self.client.delete(url)
        self.assertTrue(status.is_client_error(response.status_code))
        self.assertEqual(Transaction.objects.count(), count_transactions)

    def tearDown(self):
        self.client.logout()


class UpdateOrDeleteTransactionFromAnonym(APITestCase):
    client = APIClient()

    def setUp(self):
        user = CustomUser.objects.create_user(username='TestUser',
                                              email='testuser@mail.ru',
                                              password='password')

        category_1 = Category.objects.create(type='i', name='зар.плата', owner=user)
        category_2 = Category.objects.create(type='e', name='жкс', owner=user)

        transaction_1 = Transaction.objects.create(owner=user, category=category_1,
                                                   amount='50_000', date='2021-07-18')
        transaction_2 = Transaction.objects.create(owner=user, category=category_1,
                                                   amount='50_000', date='2021-08-18')
        transaction_3 = Transaction.objects.create(owner=user, category=category_2,
                                                   amount='3_000', date='2021-07-10')
        transaction_4 = Transaction.objects.create(owner=user, category=category_2,
                                                   amount='1_000', date='2021-07-10')

    def test_put_transaction(self):
        """попытка полного обновления транзакции"""
        old_transaction = Transaction.objects.first()
        serializer = TransactionSerializer({'pk': Transaction.objects.count()+1,
                                            'category': Category.objects.first(),
                                            'amount': 1_500, 'date': '2021-08-15'})
        url = reverse('transaction-detail', kwargs={'pk': old_transaction.pk})
        response = self.client.put(url, data=serializer.data)
        self.assertTrue(status.is_client_error(response.status_code))
        new_transaction = Transaction.objects.first()
        self.assertEqual(old_transaction, new_transaction)

    def test_patch_transaction(self):
        """попытка частичного обновления транзакции"""
        old_transaction = Transaction.objects.first()
        serializer = TransactionSerializer(old_transaction, data={'amount': 1500, }, partial=True)
        url = reverse('transaction-detail', kwargs={'pk': old_transaction.pk})
        response = self.client.patch(url, data=serializer.initial_data)
        self.assertTrue(status.is_client_error(response.status_code))
        new_transaction = Transaction.objects.first()
        self.assertEqual(old_transaction, new_transaction)

    def test_delete_transaction(self):
        """попытка удаления транзакции"""
        count_transactions = Transaction.objects.count()
        url = reverse('transaction-detail', kwargs={'pk': Transaction.objects.first().pk})
        response = self.client.delete(url)
        self.assertTrue(status.is_client_error(response.status_code))
        self.assertEqual(Transaction.objects.count(), count_transactions)
