import uuid

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from banking.exceptions import InvalidAmount
from banking.models import Account, Deposit
from banking.serializers import DepositSerializer


class DepositTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(email='test@email.com',
                                               password='testpassword')

    def test_deposit(self):
        initial_balance = 300
        deposit_amount = 100
        account = Account.objects.create(
            holder=self.user,
            balance=initial_balance,
            status=Account.ACTIVE
        )
        deposit = Deposit.make_deposit(
            account=account,
            amount=deposit_amount,
            comment='For me'
        )

        expected_balance = initial_balance + deposit_amount
        deposit = Deposit.objects.all()

        self.assertEqual(account.balance, expected_balance)
        self.assertEqual(len(deposit), 1)

    # def test_deposit_fail_amount(self):
    #     initial_balance = 0
    #     deposit_amount = 1
    #     account = Account.objects.create(
    #         holder=self.user,
    #         balance=initial_balance,
    #         status=Account.ACTIVE
    #     )
    #
    #     with self.assertRaises(InvalidAmount):
    #         Deposit.make_deposit(
    #             account=account,
    #             amount=deposit_amount,
    #             comment='For me'
    #         )

DEPOSIT_URL = reverse('banking:deposit-list')

class PublicAccountApiTest(APITestCase):

    def test_account_auth_required(self):
        res = self.client.get(DEPOSIT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateDepositApiTest(APITestCase):

    def setUp(self):
        initial_balance = 300
        deposit_amount = 100
        self.user = get_user_model().objects.create_user(email='test@email.com',
                                               password='testpassword')
        self.account = Account.objects.create(
            holder=self.user,
            balance=initial_balance,
            status=Account.ACTIVE
        )
        self.deposit = Deposit.objects.create(
            account=self.account,
            amount=deposit_amount,
            comment='For me'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_deposit_auth_required(self):
        res = self.client.get(DEPOSIT_URL)
        deposit = Deposit.objects.all().order_by('-date')
        serializer = DepositSerializer(deposit, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

    def test_deposit_limit_for_user(self):
        res = self.client.get(DEPOSIT_URL)
        deposit = Deposit.objects.filter(account=self.account)
        serializer = DepositSerializer(deposit, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 1)
        self.assertEqual(res.data['results'], serializer.data)

    def test_partial_update_account(self):
        url = DEPOSIT_URL + str(self.deposit.id) + '/'

        payload = {
            'comment': 'Hello'
        }

        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        res = self.client.patch(DEPOSIT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_full_update_account(self):
        url = DEPOSIT_URL + str(self.deposit.id) + '/'

        payload = {
            'comment': 'Hello'
        }

        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        res = self.client.patch(DEPOSIT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

