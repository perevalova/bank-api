import datetime
import uuid

from django.test import TestCase
from django.contrib.auth import get_user_model

from banking.models import Account, Customer


class ModelTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(email='test@email.com',
                                               password='testpassword')
        self.user2 = get_user_model().objects.create_user(email='test2@email.com',
                                               password='testpassword')
        self.account = Account.objects.create(
            uid=uuid.uuid4(),
            holder=self.user
        )
        self.account2 = Account.objects.create(
            uid=uuid.uuid4(),
            holder=self.user2
        )

    def test_account_instance_str(self):
        self.assertIsInstance(self.account, Account)
        self.assertEqual(self.account.__str__(), f'{self.account.uid}, {Account.INACTIVE}')

    def test_should_start_with_zero_balance(self):
        self.assertEqual(self.account.balance, 0)

    def test_status_is_inactive(self):
        self.assertEqual(self.account.status, Account.INACTIVE)

    def test_customer_instance_str(self):
        customer = Customer.objects.create(
            uid=uuid.uuid4(),
            birthday=datetime.date.today(),
            address='New York',
            passport='OP2345TY',
            phone_number='+380645789165',
            user=self.user
        )
        self.assertIsInstance(customer, Customer)
        self.assertEqual(customer.__str__(), f'{customer.uid}')
