from django.test import TestCase
from django.contrib.auth import get_user_model

from banking.exceptions import InvalidAmount
from banking.models import Account, Transaction


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
