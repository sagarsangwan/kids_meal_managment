from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required
def home(request):
    if request.method == 'GET':
        return render(request, 'pages/home.html')
    return render(request, 'pages/home.html')


def signup(request):
    print(request)
    if request.method == 'POST':
        print(request)
        user_name = request.POST['user_name']
        user_email = request.POST['user_email']
        user_password = request.POST['user_password']
        confirm_password = request.POST['confirm_password']
        print(user_name, user_email, user_password, confirm_password)

    return render(request, 'pages/signup.html')


def logoutuser(request):
    logout(request)
    return redirect('home')


def loginuser(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return render(request, 'pages/login.html')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Username or Password is incorrect')
    return render(request, 'pages/login.html')
