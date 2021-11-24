from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('login', views.signup, name="login"),
    path('register', views.register, name="register"),
    path('forgot-password', views.forgot_password, name="forgot_password"),
    path('logout', views.signout, name="logout"),
]
