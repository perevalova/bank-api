from django.contrib import admin

from banking.models import Customer, Account, Transfer, Transaction, Deposit

admin.site.register(Customer)
admin.site.register(Account)
admin.site.register(Transfer)
admin.site.register(Transaction)
admin.site.register(Deposit)
