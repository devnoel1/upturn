from django.contrib import admin

 
from .models import Orders, PaymentMethod, Account, Service, Ticket, TicketReply, Transactions

# Register your models here.
admin.site.register(Orders)
admin.site.register(PaymentMethod)
admin.site.register(Account)
admin.site.register(Service)
admin.site.register(Ticket)
admin.site.register(TicketReply)
admin.site.register(Transactions)
