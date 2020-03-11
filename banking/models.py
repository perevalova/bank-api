import uuid

from django.conf import settings
from django.db import models


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
