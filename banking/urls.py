from django.urls import path
from rest_framework.routers import DefaultRouter

from banking.views import CustomerList, CustomerDetail, AccountView, \
    TransferView, TransactionView


app_name = 'banking'

router = DefaultRouter()

router.register('account', AccountView)
router.register('transfer', TransferView)
router.register('transaction', TransactionView)

urlpatterns = [
    path('customers/', CustomerList.as_view()),
    path('customer/', CustomerDetail.as_view()),
]
urlpatterns += router.urls