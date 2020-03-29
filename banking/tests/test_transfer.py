import uuid

from django.test import TestCase
from django.contrib.auth import get_user_model

from banking.exceptions import InvalidAmount, InvalidAccount, \
    InvalidAccountReceiver
from banking.models import Account, Transfer


class TransferTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(email='test@email.com',
                                               password='testpassword')
        self.user2 = get_user_model().objects.create_user(email='test2@email.com',
                                               password='testpassword')
        self.account2 = Account.objects.create(
            uid=uuid.uuid4(),
            holder=self.user2,
            status=Account.ACTIVE
        )

    def test_transfer(self):
        initial_balance = 300
        trans_amount = 100
        account = Account.objects.create(
            holder=self.user,
            balance=initial_balance,
            status=Account.ACTIVE
        )
        Transfer.make_transfer(
            account_from=account,
            account_to=self.account2,
            amount=trans_amount,
            comment='For you'
        )

        expected_balance = initial_balance - trans_amount
        transfer = Transfer.objects.all()

        self.assertEqual(account.balance, expected_balance)
        self.assertEqual(self.account2.balance, 100)
        self.assertEqual(len(transfer), 1)

    def test_transfer_fail_amount(self):
        initial_balance = 0
        trans_amount = 100
        account = Account.objects.create(
            holder=self.user,
            balance=initial_balance,
            status=Account.ACTIVE
        )

        with self.assertRaises(InvalidAmount):
            Transfer.make_transfer(
                account_from=account,
                account_to=self.account2,
                amount=trans_amount,
                comment='For you'
            )

    def test_transfer_fail_account_to(self):
        initial_balance = 200
        trans_amount = 100
        account = Account.objects.create(
            holder=self.user,
            balance=initial_balance,
            status=Account.ACTIVE
        )

        with self.assertRaises(InvalidAccount):
            Transfer.make_transfer(
                account_from=account,
                account_to=account,
                amount=trans_amount,
                comment='For you'
            )

    def test_transfer_fail_account_status(self):
        initial_balance = 200
        trans_amount = 100
        user = get_user_model().objects.create_user(
            email='test3@email.com',
            password='testpassword')
        account2 = Account.objects.create(
            uid=uuid.uuid4(),
            holder=user,
            status=Account.INACTIVE
        )
        account = Account.objects.create(
            holder=self.user,
            balance=initial_balance,
            status=Account.ACTIVE
        )

        with self.assertRaises(InvalidAccountReceiver):
            Transfer.make_transfer(
                account_from=account,
                account_to=account2,
                amount=trans_amount,
                comment='For you'
            )
