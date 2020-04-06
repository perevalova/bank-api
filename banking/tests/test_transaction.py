from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from banking.exceptions import InvalidAmount
from banking.models import Account, Transaction
from banking.serializers import TransactionSerializer

TRANSACTION_URL = reverse('banking:transaction-list')

class TransactionTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(email='test@email.com',
                                               password='testpassword')

    def test_transaction(self):
        initial_balance = 300
        trans_amount = 100
        account = Account.objects.create(
            holder=self.user,
            balance=initial_balance,
            status=Account.ACTIVE
        )
        Transaction.make_transaction(
            account=account,
            merchant='GH',
            amount=trans_amount,
            comment='For you'
        )

        expected_balance = initial_balance - trans_amount
        transaction = Transaction.objects.all()

        self.assertEqual(account.balance, expected_balance)
        self.assertEqual(len(transaction), 1)

    def test_transaction_fail_amount(self):
        initial_balance = 0
        trans_amount = 100
        account = Account.objects.create(
            holder=self.user,
            balance=initial_balance,
            status=Account.ACTIVE
        )

        with self.assertRaises(InvalidAmount):
            Transaction.make_transaction(
                account=account,
                merchant='GH',
                amount=trans_amount,
                comment='For you'
            )


class PublicTransactionApiTest(APITestCase):

    def test_transaction_auth_required(self):
        res = self.client.get(TRANSACTION_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTransactionApiTest(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(email='test@email.com',
                                               password='testpassword')
        initial_balance = 300
        self.account = Account.objects.create(
            holder=self.user,
            balance=initial_balance
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        trans_amount = 100
        Transaction.objects.create(
            account=self.account,
            merchant='GH',
            amount=trans_amount,
            comment='For you'
        )

    def test_transaction_auth_required(self):
        res = self.client.get(TRANSACTION_URL)
        transaction = Transaction.objects.all().order_by('-date')
        serializer = TransactionSerializer(transaction, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

    def test_transaction_limit_for_account(self):
        user = get_user_model().objects.create_user(email='test2@email.com',
                                                    password='testpassword')
        initial_balance = 200
        account = Account.objects.create(
            holder=user,
            balance=initial_balance
        )
        trans_amount = 100
        Transaction.objects.create(
            account=account,
            merchant='GH',
            amount=trans_amount,
            comment='For you'
        )
        res = self.client.get(TRANSACTION_URL)
        transaction = Transaction.objects.filter(account=self.account)
        serializer = TransactionSerializer(transaction, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 1)
        self.assertEqual(res.data['results'], serializer.data)
