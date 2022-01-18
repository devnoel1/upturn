from coinbase_commerce.api_resources import event
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.http import HttpResponse

from dashboard.forms import AccountForm, OrdersForm, TicketForm, TicketReplyForm
from dashboard.models import Account, Orders, PaymentMethod, Service, Ticket, TicketReply, Transactions, User
from dashboard.payments.Coinbase import Coinbase
from dashboard.payments.PayStack import PayStack
from dashboard.payments.update_account import UserAccount
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from coinbase_commerce.error import WebhookInvalidPayload, SignatureVerificationError
from django.http import JsonResponse
from django.core import serializers


# Create your views here.
def dashboard(request):
    args = {}
    args['page_title'] = 'new order'
    args['form'] = OrdersForm
    args['services'] = Service.objects.all()

    return render(request, 'dashboard/index.html',args)

def make_order(request):
    if request.method == "POST":
        service_id = request.POST['service']
        service = Service.objects.get(pk=service_id)

        account = Account.objects.get(user=request.user.pk)

        balance = account.balance

        # return HttpResponse(account.balance)
        
        if float(balance) >= float(service.price):
            new_balance = float(balance) - float(service.price)
            orders = Orders(user = request.user, service = service, status=1)
            orders.save()
            accoun_model = Account.objects.filter(user=request.user).update(balance=new_balance)

            messages.success(request, 'Service Purchased Successfuly')
        else:
            messages.error(request, 'You dont have surficiant amount to purchase this service')

    return redirect('dashboard')


def service(request):
    args = {}
    args['page_title'] = 'service'
    args['services'] = Service.objects.all()

    return render(request, 'dashboard/service.html',args)

def service_details(request):
    args = {}
    service = serializers.serialize('json',Service.objects.filter(pk=request.GET.get('id')))
    
    return JsonResponse({'data':service})
        
def orders(request):
    args = {}
    args['page_title'] = 'orders'
    args['orders'] = Orders.objects.filter(user=request.user)

    return render(request, 'dashboard/orders.html',args)

def add_founds(request):
    args = {}
    args['page_title'] = 'add founds'
    args['payment_methods'] = PaymentMethod.objects.all()
    args['transactions'] = Transactions.objects.filter(user=request.user.pk)

    if request.method == "POST":
        method = request.POST['payment_method']
        amount = float(request.POST['amount'])

        if method == 'coinbase':
            coinbase_obj = Coinbase()
            coinbase = coinbase_obj.createCharge(amount,request.user,method='coinbase')
            return HttpResponseRedirect(coinbase['hosted_url'])
            
        elif method == 'paystack':
            paystack_obj = PayStack()
            paystack = paystack_obj.make_transaction(amount, request.user, method='paystack')
            # return  HttpResponseHttpResponse(paystack)
            return HttpResponseRedirect(paystack)
            
    return render(request, 'dashboard/add-founds.html',args)

def paystack_callback(request):
    args={}
    ref = request.GET['reference']
    paystack_obj = PayStack()
    verify = paystack_obj.verify_payment(ref=ref) 

    if verify[0] == 200:
        UserAccount.update_users_account(request.user.pk,verify[3]['requested_amount'])
        UserAccount.update_transaction(ref,'1')
        messages.success(request, 'Your Account is Credited Successfuly')
    else:
        messages.error(request, 'Your Account is not Credited Successfuly')

    return redirect(add_founds)

def coinbase_success(request):
    messages.success(request, 'Your Transaction is sent successfuly, awaiting approval')
    return

def coinbase_cancel(request):
    messages.error(request, 'You have canceled your transaction')
    return redirect(add_founds)

@csrf_exempt
def coinbase_webhook(request):
    # event payload
    request_data = request.body.decode('utf-8')
    # webhook signature
    request_sig = request.headers.get('X-CC-Webhook-Signature', None)

    coinbase_obj = Coinbase()

    try:
        # signature verification and event object construction
        event = coinbase_obj.webhooks(request_data,request_sig)
    except (WebhookInvalidPayload, SignatureVerificationError) as e:
        return str(e), 400
    
    if (event.type == 'charge:pending'):
         UserAccount.update_transaction(event.id,'0')
         messages.warning(request, 'Your Transaction is still pending')
    elif (event.type == 'charge:confirmed'):
        UserAccount.update_transaction(event.id,'1')
        messages.success(request, 'Your Account is Credited Successfuly')
    elif (event.type == 'charge:failed'):
        UserAccount.update_transaction(event.id,'-1')
        messages.error(request, 'Transaction failed')
   
    print("Received event: id={id}, type={type}".format(id=event.id, type=event.type))
    return 'success', 200

def affiliate(request):
    args = {}
    args['page_title'] = 'affiliate'
    return render(request, 'dashboard/affiliate.html',args)

def ticket(request):
    args = {}
    args['tickets'] = Ticket.objects.all()
    args['page_title'] = 'ticket'
    if request.method == "POST":
        form = TicketForm(request.POST)

        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            args['success'] = 'Ticket is Opened Successfuly'

    return render(request, 'dashboard/ticket.html',args)

def ticket_details(request, id):
    args = {}
    args['details'] = TicketReply.objects.filter(ticket=id) 
    args['page_title'] = 'tickets details'

    return render(request, 'dashboard/tickets_details.html',args)

def profile(request):
    args = {}
    args['page_title'] = 'profile'
    return render(request, 'dashboard/mass-order.html',args)

def subscription(request):
    args = {}
    args['page_title'] = 'subscription'
    args['subscriptions'] = Orders.objects.filter(user=request.user.id)
    return render(request, 'dashboard/subscription.html',args)