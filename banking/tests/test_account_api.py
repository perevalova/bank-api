import uuid

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from banking.models import Account
from banking.serializers import AccountSerializer


ACCOUNT_URL = reverse('banking:account-list')

class PublicAccountApiTest(APITestCase):

    def test_account_auth_required(self):
        res = self.client.get(ACCOUNT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAccountApiTest(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(email='test@email.com',
                                               password='testpassword')
        self.account = Account.objects.create(
            uid=uuid.uuid4(),
            holder=self.user
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_account_auth_required(self):
        res = self.client.get(ACCOUNT_URL)
        account = Account.objects.all().order_by('-created')
        serializer = AccountSerializer(account, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

    def test_account_limit_for_user(self):
        user2 = get_user_model().objects.create_user(email='test2@email.com',
                                                    password='testpassword')
        account2 = Account.objects.create(
            uid=uuid.uuid4(),
            holder=user2
        )
        res = self.client.get(ACCOUNT_URL)
        account = Account.objects.filter(holder=self.user)
        serializer = AccountSerializer(account, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 1)
        self.assertEqual(res.data['results'], serializer.data)

    def test_create_account_always_zero(self):
        user = get_user_model().objects.create_user(email='test3@email.com',
                                               password='testpassword')
        client = APIClient()
        client.force_authenticate(user=user)
        payload = {'balance': 10000.50}
        res = client.post(ACCOUNT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        account = Account.objects.get(uid=res.data['uid'])
        self.assertEqual(0, account.balance)

    def test_partial_update_account(self):
        url = ACCOUNT_URL + str(self.account.uid) + '/'

        payload = {
            'balance': 9999999
        }

        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        res = self.client.patch(ACCOUNT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_full_update_account(self):
        url = ACCOUNT_URL + str(self.account.uid) + '/'

        payload = {
            'balance': 9999999,
            'status': Account.ACTIVE
        }

        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        res = self.client.patch(ACCOUNT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

