from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from banking.models import Account, Withdrawal
from banking.serializers import WithdrawalSerializer


class WithdrawalTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(email='test@email.com',
                                               password='testpassword')

    def test_withdrawal(self):
        initial_balance = 300
        withdrawal_amount = 100
        account = Account.objects.create(
            holder=self.user,
            balance=initial_balance,
            status=Account.ACTIVE
        )
        Withdrawal.make_withdrawal(
            account=account,
            amount=withdrawal_amount,
        )

        expected_balance = initial_balance - withdrawal_amount
        withdrawal = Withdrawal.objects.all()

        self.assertEqual(account.balance, expected_balance)
        self.assertEqual(len(withdrawal), 1)

WITHDRAWAL_URL = reverse('banking:withdrawal-list')

class PublicWithdrawalApiTest(APITestCase):

    def test_account_auth_required(self):
        res = self.client.get(WITHDRAWAL_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateWithdrawalApiTest(APITestCase):

    def setUp(self):
        initial_balance = 300
        withdrawal_amount = 100
        self.user = get_user_model().objects.create_user(email='test@email.com',
                                               password='testpassword')
        self.account = Account.objects.create(
            holder=self.user,
            balance=initial_balance,
            status=Account.ACTIVE
        )
        self.withdrawal = Withdrawal.objects.create(
            account=self.account,
            amount=withdrawal_amount,
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_withdrawal_auth_required(self):
        res = self.client.get(WITHDRAWAL_URL)
        withdrawal = Withdrawal.objects.all().order_by('-date')
        serializer = WithdrawalSerializer(withdrawal, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

    def test_withdrawal_limit_for_user(self):
        res = self.client.get(WITHDRAWAL_URL)
        withdrawal = Withdrawal.objects.filter(account=self.account)
        serializer = WithdrawalSerializer(withdrawal, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 1)
        self.assertEqual(res.data['results'], serializer.data)

    def test_partial_update_withdrawal(self):
        url = WITHDRAWAL_URL + str(self.withdrawal.id) + '/'

        payload = {
            'amount': 50
        }

        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        res = self.client.patch(WITHDRAWAL_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_full_update_withdrawal(self):
        url = WITHDRAWAL_URL + str(self.withdrawal.id) + '/'

        payload = {
            'amount': 50
        }

        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        res = self.client.patch(WITHDRAWAL_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
