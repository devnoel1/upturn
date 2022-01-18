from dashboard.models import Account

def add_variable_to_context(request):
    if Account.objects.filter(user=request.user.pk).exists():
        account =  Account.objects.get(user=request.user.pk)
        account = account.balance
    else:
        account = '0.00'
   
    return {
        'account_balance':account
    }