from django.urls import path

from . import views

urlpatterns = [
    path('dashboard',views.dashboard, name="dashboard"),
    path('service',views.service, name="serivce"),
    path('orders',views.orders, name="orders"),
    path('add-founds',views.add_founds, name="add-founds"),
    path('affiliate',views.affiliate, name="affiliate"),
    path('ticket',views.ticket, name="ticket"),
    path('mass-order',views.mass_order, name="mass-order"),
]