from django.urls import path

from . import views

urlpatterns = [
    path('groupAdder', views.groupAdder, name="groupAdder"),
    path('bot', views.bot, name="bot"),
]