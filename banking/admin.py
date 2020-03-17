from django.contrib import admin

from banking.models import Customer, Account


admin.site.register(Customer)
admin.site.register(Account)
