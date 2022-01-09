from django.urls import path

from . import views

urlpatterns = [
    path('dashboard',views.dashboard, name="dashboard"),
    path('make_order',views.make_order, name="make_order"),
    path('service',views.service, name="serivce"),
    path('service_details',views.service_details, name="service_details"),
    path('orders',views.orders, name="orders"),
    path('add-founds',views.add_founds, name="add-founds"),
    path('affiliate',views.affiliate, name="affiliate"),
    path('ticket',views.ticket, name="ticket"),
    path('ticket/<int:id>',views.ticket_details),
    path('profile',views.profile, name="profile"),
    path('subscription',views.subscription, name="subscription"),
    path('paystack_callback',views.paystack_callback),
    path('coinbase_success',views.coinbase_success),
    path('coinbase_cancel',views.coinbase_cancel),
    path('coinbase_webhook',views.coinbase_webhook),
]
