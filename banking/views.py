import requests
from sys import exc_info

from rest_framework import generics, status, mixins, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView

from banking.exceptions import InvalidAmount, InvalidAccount, \
    InvalidAccountReceiver
from banking.models import Customer, Account, Transfer, Transaction, Deposit
from banking.serializers import CustomerSerializer, CustomerUserSerializer, \
    AccountSerializer, TransferSerializer, TransactionSerializer, \
    DepositSerializer


class CustomerList(generics.ListCreateAPIView):
    """
    View customer list for current user
    """
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class CustomerDetail(generics.RetrieveUpdateAPIView):
    """
    Customer detail with User form
    """
    serializer_class = CustomerUserSerializer
    queryset = Customer.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.queryset.filter(user=self.request.user).first()


class AccountView(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()
    lookup_field = 'uid'
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """ Return object for current authenticated user only """
        return self.queryset.filter(holder=self.request.user)

    @action(methods=['put'], detail=True)
    def activate(self, request, **kwargs):
        """ Change account status to active """
        account = self.get_object()
        account.status = Account.ACTIVE
        account.save()

        return Response(status=status.HTTP_200_OK)

    @action(methods=['put'], detail=True)
    def deactivate(self, request, **kwargs):
        """ Change account status to inactive """
        account = self.get_object()
        account.status = Account.INACTIVE
        account.save()

        return Response(status=status.HTTP_200_OK)

    @action(methods=['put'], detail=True)
    def block(self, request, **kwargs):
        """ Change account status to block """
        account = self.get_object()
        account.status = Account.BLOCKED
        account.save()

        return Response(status=status.HTTP_200_OK)


class TransferView(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin):
    """
    Make transfer from account to another account
    """
    serializer_class = TransferSerializer
    queryset = Transfer.objects.all()
    permission_classes = (IsAuthenticated,)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['account_to']
    ordering_fields = ['account_to', 'date']

    def get_queryset(self):
        account = Account.objects.filter(holder_id=self.request.user)
        return self.queryset.filter(account_from__in=account)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            Transfer.make_transfer(**serializer.validated_data)
        except (InvalidAmount, InvalidAccount, InvalidAccountReceiver):
            error_type, error, tb = exc_info() # get error message and status code
            content = {'error': error.detail}
            status_code = error.status_code
            return Response(content, status=status_code)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TransactionView(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    """
    Make transaction from account to merchant
    """
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    permission_classes = (IsAuthenticated,)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['merchant']
    ordering_fields = ['merchant', 'date']

    def get_queryset(self):
        account = Account.objects.filter(holder_id=self.request.user)
        return self.queryset.filter(account__in=account)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            Transaction.make_transaction(**serializer.validated_data)
        except InvalidAmount:
            error_type, error, tb = exc_info() # get error message and status code
            content = {'error': error.detail}
            status_code = error.status_code
            return Response(content, status=status_code)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DepositView(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    """
    Make deposit to account
    """
    serializer_class = DepositSerializer
    queryset = Deposit.objects.all()
    permission_classes = (IsAuthenticated,)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['date']

    def get_queryset(self):
        account = Account.objects.filter(holder_id=self.request.user)
        return self.queryset.filter(account__in=account)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            Deposit.make_deposit(**serializer.validated_data)
        except InvalidAmount:
            error_type, error, tb = exc_info() # get error message and status code
            content = {'error': error.detail}
            status_code = error.status_code
            return Response(content, status=status_code)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CurrencyRate(APIView):
    """
    View currency exchange rate.
    USD, EUR, RUR, BTC
    """
    def get(self, request, format=None):
        url = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=11'
        currency = requests.get(url)
        return Response(currency.json())
