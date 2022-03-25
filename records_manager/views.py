from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
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
        user_name = request.POST['user_name']
        user_email = request.POST['user_email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        user_password = request.POST['user_password']
        confirm_password = request.POST['confirm_password']
        print(user_name, user_email, user_password,
              confirm_password, first_name, last_name)
        if user_password == confirm_password:
            if User.objects.filter(username=user_name).exists():
                messages.info(request, 'Username already taken')
                return redirect('signup')
            elif User.objects.filter(email=user_email).exists():
                messages.info(request, 'Email already taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(
                    username=user_name, password=user_password, email=user_email, first_name=first_name, last_name=last_name)
                user.save()
                messages.info(request, 'User created')
                return redirect('login')
        else:
            messages.info(request, 'Password not matching')
            return redirect('signup')

    return render(request, 'pages/signup.html')


def logoutuser(request):
    logout(request)
    messages.success(request, 'Logged out Successfully')
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
            messages.success(request, 'Logged in Successfully')
            return redirect('/')
        else:
            messages.error(request, 'Username or Password is incorrect')
    return render(request, 'pages/login.html')
