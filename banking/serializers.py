import decimal
import requests

from django.core.validators import RegexValidator
from rest_framework import serializers

from banking.models import Customer, Account
from users.serializers import CustomUserSerializer


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


class CustomerUserSerializer(CustomerSerializer):
    user = CustomUserSerializer()


class AccountSerializer(serializers.ModelSerializer):
    holder = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    balance_usd = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ('uid', 'balance', 'holder', 'created', 'status', 'balance_usd')
        read_only_fields = ('uid', 'balance','holder',  'created', 'status', 'balance_usd')

    def get_balance_usd(self, obj):
        """
        Account balance in USD
        """
        url = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=11'
        get_currency = requests.get(url)
        decimal.getcontext().prec = 2 # set new precision
        currency = get_currency.json()[0]['sale'] # currency exchange for UAH to USD
        return obj.balance/decimal.Decimal(currency)
