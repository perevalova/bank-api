from django.urls import path
from banking.views import CustomerList, CustomerDetail


urlpatterns = [
    path('customers/', CustomerList.as_view()),
    path('customer/', CustomerDetail.as_view()),
]
