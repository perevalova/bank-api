import datetime
import uuid

from django.test import TestCase
from django.contrib.auth import get_user_model

from banking.models import Account, Customer, Deposit, Withdrawal, Transfer, \
    Transaction


class AccountModelTests(TestCase):
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


class CustomerModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email='test@email.com',
                                               password='testpassword')

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


class TransferModelTests(TestCase):
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
        transfer = Transfer.objects.all().first()

        self.assertIsInstance(transfer, Transfer)
        self.assertEqual(transfer.__str__(), f'{transfer.account_from} - {transfer.account_to}')


class TransactionModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email='test@email.com',
                                               password='testpassword')

    def test_transfer(self):
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
        transaction = Transaction.objects.all().first()

        self.assertIsInstance(transaction, Transaction)
        self.assertEqual(transaction.__str__(), f'Account {transaction.account.uid} sent {transaction.amount} to {transaction.merchant}')


class DepositModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email='test@email.com',
                                               password='testpassword')
        self.account = Account.objects.create(
            uid=uuid.uuid4(),
            holder=self.user
        )

    def test_deposit_instance_str(self):
        deposit_amount = 100
        deposit = Deposit.objects.create(
            account=self.account,
            amount=deposit_amount,
            comment='For me'
        )

        self.assertIsInstance(deposit, Deposit)
        self.assertEqual(deposit.__str__(), f'Account {self.account.uid} made a {deposit.amount} deposit')


class WithdrawalModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email='test@email.com',
                                               password='testpassword')
        self.account = Account.objects.create(
            uid=uuid.uuid4(),
            holder=self.user
        )
        deposit_amount = 100
        Deposit.objects.create(
            account=self.account,
            amount=deposit_amount,
            comment='For me'
        )

    def test_deposit_instance_str(self):
        withdrawal_amount = 100
        withdrawal = Withdrawal.objects.create(
            account=self.account,
            amount=withdrawal_amount
        )

        self.assertIsInstance(withdrawal, Withdrawal)
        self.assertEqual(withdrawal.__str__(), f'Account {self.account.uid} made withdrawal a {withdrawal.amount}')
