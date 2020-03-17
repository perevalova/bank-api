import uuid

from django.conf import settings
from django.db import models


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
