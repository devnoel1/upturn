from django.http import response
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from dashboard.models import Account


# Create your views here.
def index(request):
    return render(request, 'pages/index.html')

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('user/dashboard')
        else:
            messages.warning(request,"Invalid Login Creadentials")

    if request.user.is_authenticated:
        return redirect('user/dashboard')

    return render(request, 'auth/login.html')

def register(request):
    if request.method == "POST":
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if User.objects.filter(email=email):
            messages.warning(request,"email address already exist!")
            return redirect('register')

        if User.objects.filter(username=username):
            messages.warning(request,"username already exist!")
            return redirect('register')

        if password != confirm_password:
            messages.warning(request, "Password field does not match")
            return redirect('register')

        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        user = authenticate(username=username, password=password)

        account = Account(user=user)
        account.save()

        if user is not None:
            login(request, user)
            return redirect('user/dashboard')

    if request.user.is_authenticated:
        return redirect('user/dashboard')

    return render(request, 'auth/register.html')

def forgot_password(request):
    if request.method == "POST":
        pass

    return render(request, 'auth/forgot-password.html')

def signout(request):
    logout(request)
    return redirect('home')