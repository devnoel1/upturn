from django.db import models
from django.db.models.fields.related import ForeignKey
from django.contrib.auth import get_user_model

User = get_user_model()

class Service(models.Model):
    name = models.CharField(max_length=225)
    description = models.TextField(blank=True)
    price = models.CharField(max_length=225,default=0.00, blank=True)
    duration = models.CharField(max_length=225, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f"{self.name}"

# Create your models here.
class Orders(models.Model):
    options = (
        ('1','approved'),
        ('0','pending'),
        ('-1','expired')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=options, default=0)
    link = models.CharField(max_length=225, blank=True, null=True)
    quantity = models.CharField(max_length=225, blank=True,null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f"{self.user} {self.service}"

class PaymentMethod(models.Model):
    name = models.CharField(max_length=225)
    api_key = models.TextField(blank=True, null=True)
    secrete_key = models.TextField(blank=True, null=True)
    primary_key = models.TextField(blank=True, null=True)
    slug = models.CharField(max_length=225, null=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f"{self.name}"

class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.CharField(max_length=225, default=0.00)
    created_on = models.DateTimeField(auto_now_add=True) 

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f"{self.user} {self.balance}"

class Ticket(models.Model):
    options = (
        ('0','pending'),
        ('1','answered'),
        ('-1','closed')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=225)
    status = models.CharField(max_length = 150, choices=options, default=0)
    created_on = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.subject}"

class TicketReply(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    message = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.ticket}"

class Transactions(models.Model):
    options = (
        ('0','pending'),
        ('1','successful'),
        ('-1','failed')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.CharField(max_length=225, default=0.00)
    trans_type = models.CharField(max_length=225, null=True)
    method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, null=True, blank=True)
    trans_ref = models.CharField(max_length=225, null=True, blank=True)
    status = models.CharField(max_length = 150, choices=options, default=0)
    created_on = models.DateTimeField(auto_now_add=True) 
    def __str__(self):
        return f"{self.user} {self.trans_ref}"