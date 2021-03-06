from django.urls import path
from rest_framework.routers import DefaultRouter

from banking.views import CustomerList, CustomerDetail, AccountView, \
    TransferView, TransactionView, CurrencyRate, DepositView, WithdrawalView

app_name = 'banking'

router = DefaultRouter()

router.register('account', AccountView)
router.register('transfer', TransferView)
router.register('transaction', TransactionView)
router.register('deposit', DepositView)
router.register('withdrawal', WithdrawalView)

urlpatterns = [
    path('customers/', CustomerList.as_view(), name='customers'),
    path('customer/', CustomerDetail.as_view(), name='customer'),
    path('currency/', CurrencyRate.as_view(), name='currency'),
]
urlpatterns += router.urls