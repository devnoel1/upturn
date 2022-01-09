from django import forms
from django.core.checks import messages
from django.core.exceptions import ValidationError
from django.forms import fields

from dashboard.models import  Orders, Ticket, Account

class AccountForm(forms.ModelForm):
  
    class Meta:
        model = Account
        fields = ['balance']

class OrdersForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['service','link','quantity']


class TicketForm(forms.ModelForm):
    subject = forms.CharField(max_length=225)

    class Meta:
        model=Ticket
        fields = ['subject']

    def clean_renewal_date(self):
        data = self.cleaned_data['subject']

        if data == '':
            raise ValidationError(_('Subject Field cannot be empty'))

        return data

class TicketReplyForm(forms.ModelForm):
    messages = forms.Textarea()
    
