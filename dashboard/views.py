from django.shortcuts import render

# Create your views here.
def dashboard(request):
    args = {}
    args['page_title'] = 'new order'
    return render(request, 'dashboard/index.html',args)

def service(request):
    args = {}
    args['page_title'] = 'service'
    return render(request, 'dashboard/service.html',args)

def orders(request):
    args = {}
    args['page_title'] = 'orders'
    return render(request, 'dashboard/orders.html',args)

def add_founds(request):
    args = {}
    args['page_title'] = 'add founds'
    return render(request, 'dashboard/add-founds.html',args)

def affiliate(request):
    args = {}
    args['page_title'] = 'affiliate'
    return render(request, 'dashboard/affiliate.html',args)

def ticket(request):
    args = {}
    args['page_title'] = 'ticket'
    return render(request, 'dashboard/ticket.html',args)

def mass_order(request):
    args = {}
    args['page_title'] = 'mass order'
    return render(request, 'dashboard/mass-order.html',args)