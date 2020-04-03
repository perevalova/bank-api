import datetime
import uuid

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from banking.models import Account, Customer
from banking.serializers import AccountSerializer, CustomerSerializer

CUSTOMER_URL = reverse('banking:customer')

class PublicCustomerApiTest(APITestCase):

    def test_account_auth_required(self):
        res = self.client.get(CUSTOMER_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCustomerApiTest(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(email='test@email.com',
                                               password='testpassword')

        self.customer = Customer.objects.create(
            uid=uuid.uuid4(),
            birthday=datetime.date.today(),
            address='New York',
            passport='OP2345TY',
            phone_number='+380645789165',
            user=self.user
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_customer_auth_required(self):
        res = self.client.get(CUSTOMER_URL)
        customer = Customer.objects.all()
        serializer = CustomerSerializer(customer)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # self.assertEqual(res.data, serializer.data)

    def test_customer_limit_for_user(self):
        user2 = get_user_model().objects.create_user(email='test2@email.com',
                                                    password='testpassword')
        customer2 = Customer.objects.create(
            uid=uuid.uuid4(),
            birthday=datetime.date.today(),
            address='London',
            passport='YI345678OP',
            phone_number='+380645789165',
            user=user2
        )
        res = self.client.get(CUSTOMER_URL)
        customer = Customer.objects.filter(user=self.user)
        serializer = CustomerSerializer(customer, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # self.assertEqual(len(res.data['results']), 1)
        # self.assertEqual(res.data, serializer.data)

    def test_partial_update_account(self):
        data = {
            'birthday': datetime.date.today(),
            'address': 'Kyiv',
            'passport': 'LG546364ED',
            'phone_number': '+380945768213',
        }

        res = self.client.patch(CUSTOMER_URL, data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.address, data['address'])

    def test_full_update_account(self):

        data = {
            'address': 'Caroline'
        }

        res = self.client.patch(CUSTOMER_URL, data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.address, data['address'])

