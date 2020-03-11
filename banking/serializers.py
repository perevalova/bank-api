from django.core.validators import RegexValidator
from rest_framework import serializers

from banking.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    phone_number = serializers.CharField(
        min_length=13,
        max_length=13,
        validators=[RegexValidator(
            r'^(\+380)?\d{9}$',
            message="Phone number must be entered in the format: +380999999999")]
    )

    class Meta:
        model = Customer
        fields = ('uid', 'user', 'birthday', 'address', 'passport', 'phone_number')
