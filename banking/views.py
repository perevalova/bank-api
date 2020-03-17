from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets

from banking.models import Customer, Account
from banking.serializers import CustomerSerializer, CustomerUserSerializer, \
    AccountSerializer


class CustomerList(generics.ListCreateAPIView):
    """
    View customer list for current user
    """
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class CustomerDetail(generics.RetrieveUpdateAPIView):
    """
    Customer detail with User form
    """
    serializer_class = CustomerUserSerializer
    queryset = Customer.objects.all()

    def get_object(self):
        return self.queryset.filter(user=self.request.user).first()



class AccountView(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()
    lookup_field = 'uid'

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
