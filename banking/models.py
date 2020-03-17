import uuid
from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models, transaction


class AccountActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Account.ACTIVE)


class Customer(models.Model):
    uid = models.UUIDField(
        unique=True,
        editable=False,
        db_index=True,
        default=uuid.uuid4()
    )
    birthday = models.DateField()
    address = models.CharField(
        max_length=255
    )
    passport = models.CharField(
        max_length=20
    )
    phone_number = models.CharField(
        max_length=13
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.uid


class Account(models.Model):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    BLOCKED = 'blocked'
    STATUS_CHOICES = (
        (ACTIVE, 'active'),
        (INACTIVE, 'inactive'),
        (BLOCKED, 'blocked'),
    )

    uid = models.UUIDField(
        unique=True,
        editable=False,
        db_index=True,
        default=uuid.uuid4,
        verbose_name='Public identifier',
    )
    holder = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )
    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )
    created = models.DateTimeField(
        auto_now_add=True
    )
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=10,
        default=INACTIVE
    )

    objects = models.Manager() # Default manager
    active = AccountActiveManager()  # New manager for active accounts

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.uid}, {self.status}'


class Transfer(models.Model):
    account_from = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='account_from'
    )
    account_to = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='account_to'
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    date = models.DateTimeField(
        auto_now_add=True
    )
    comment = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f'{self.account_from} - {self.account_to}'

    @classmethod
    def make_transfer(cls, account_from, account_to, amount, comment):
        if account_from.balance < amount:
            raise (ValueError('Not enough money on balance!!!'))
        if account_from == account_to:
            raise (ValueError('Type another account!'))
        if account_to.status == Account.INACTIVE or account_to.status == Account.BLOCKED:
            raise (ValueError('Account of receiver is inactive or blocked!'))

        with transaction.atomic():
            account_from.balance -= amount
            account_from.save()

            account_to.balance += amount
            account_to.save()

            transfer = cls.objects.create(
                account_from=account_from,
                account_to=account_to,
                amount=amount,
                comment=comment
            )

        return account_from, account_to, transfer

