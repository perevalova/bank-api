from rest_framework import generics

from banking.models import Customer
from banking.serializers import CustomerSerializer


class CustomerList(generics.ListCreateAPIView):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class CustomerDetail(generics.RetrieveUpdateAPIView):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()

    def get_object(self):
        return self.queryset.filter(user=self.request.user).first()
