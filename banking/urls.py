from django.urls import path
from rest_framework.routers import DefaultRouter

from banking.views import CustomerList, CustomerDetail, AccountView, \
    TransferView, TransactionView, CurrencyRate


app_name = 'banking'

router = DefaultRouter()

router.register('account', AccountView)
router.register('transfer', TransferView)
router.register('transaction', TransactionView)

urlpatterns = [
    path('customers/', CustomerList.as_view()),
    path('customer/', CustomerDetail.as_view()),
    path('currency/', CurrencyRate.as_view(), name='currency'),
]
urlpatterns += router.urls