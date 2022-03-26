from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required
def home(request):
    if request.method == 'GET':
        all_kid = child.objects.filter(user_id=request.user)
        for kid in all_kid:
            print(kid.parent_email)
        current_user = request.user
        return render(request, 'pages/home.html', {'all_kid': all_kid, 'current_user_name': current_user.first_name+' '+current_user.last_name})

    return render(request, 'pages/home.html')


@login_required
def add_child(request):
    user_id = request.user.id
    kid_name = request.POST['kid_name']
    kid_age = request.POST['kid_age']
    parent_phone = request.POST['parent_phone']
    parent_email = request.POST['parent_email']
    if user_id and kid_name and kid_age and parent_phone and parent_email:
        print(user_id, kid_name, kid_age, parent_phone, parent_email)
        child_info = child(user_id=request.user, name=kid_name, age=kid_age,
                           parent_contact_number=parent_phone, parent_email=parent_email)
        child_info.save()
        messages.success(request, 'Child added successfully')
        return redirect('home')
    else:
        messages.error(request, 'Please fill all the fields')
        return redirect('home')


@login_required
def kid_info(request, id):
    if request.method == 'GET':
        kid_info = child.objects.get(id=id)
        meal_info = kid_meal.objects.filter(kid_id=id)

        return render(request, 'pages/kid_info.html', {'kid_id': id, 'kid_name': kid_info.name, 'kid_age': kid_info.age, 'parent_email': kid_info.parent_email, 'parent_phone': kid_info.parent_contact_number, 'meal_info': meal_info, 'current_user_name': request.user.first_name+' '+request.user.last_name})


@login_required
def add_meal(request, id):
    kid = child.objects.get(id=id)
    img_url = request.POST['img_url']
    food_group = request.POST['food_group']

    if img_url and food_group:
        is_approved = food_group != 'Unknown'
        meal_info = kid_meal(kid_id=kid, image_url=img_url, food_group=food_group,
                             approved_by=request.user, is_approved=is_approved)
        meal_info.save()
        messages.success(request, 'Meal added successfully')
        return redirect('kid_info', id=id)
    else:
        messages.error(request, 'Please fill all the fields')
        return redirect('kid_info', id=id)


@login_required
def edit_kid_info(request, id):
    kid_info = child.objects.get(id=id)
    kid_info.name = request.POST['kid_name']
    kid_info.age = request.POST['kid_age']
    kid_info.parent_email = request.POST['parent_email']
    kid_info.parent_contact_number = request.POST['parent_phone']
    kid_info.save()
    messages.success(request, 'Child updated successfully')
    return redirect('kid_info', id=id)


@login_required
def delete_kid(request, id):
    if request.method == 'GET':
        child_info = child.objects.get(id=id)
        child_info.delete()
        messages.success(request, 'Child deleted successfully')
        return redirect('home')


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
                messages.error(request, 'Username already taken')
                return render(request, 'pages/signup.html', {
                    'user_name': user_name,
                    'user_email': user_email,
                    'first_name': first_name,
                    'last_name': last_name,
                })
            elif User.objects.filter(email=user_email).exists():
                messages.error(request, 'Email already taken')
                return render(request, 'pages/signup.html', {
                    'user_name': user_name,
                    'user_email': user_email,
                    'first_name': first_name,
                    'last_name': last_name,
                })
            else:
                user = User.objects.create_user(
                    username=user_name, password=user_password, email=user_email, first_name=first_name, last_name=last_name)
                user.save()
                messages.error(request, 'User created')
                return redirect('login')
        else:
            messages.error(request, 'Password not matching')
            return render(request, 'pages/signup.html', {
                'user_name': user_name,
                'user_email': user_email,
                'first_name': first_name,
                'last_name': last_name,
            })
    else:
        return render(request, 'pages/signup.html', {
            'user_name': '',
            'user_email': '',
            'first_name': '',
            'last_name': '',
        })


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
