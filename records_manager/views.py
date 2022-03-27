from datetime import timezone
import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings


# home page for displaying all the records of current user
@login_required
def home(request):
    if request.method == 'GET':
        # getting all kid records of current user and displaying them on home page
        all_kid = child.objects.filter(user_id=request.user)
        current_user = request.user
        return render(request, 'pages/home.html', {'all_kid': all_kid, 'current_user_name': current_user.first_name+' '+current_user.last_name})

    return render(request, 'pages/home.html')


# add kid page for adding new kid to the database of current user

@login_required
def add_kid(request):
    user_id = request.user.id
    kid_name = request.POST['kid_name']
    kid_age = request.POST['kid_age']
    parent_phone = request.POST['parent_phone']
    parent_email = request.POST['parent_email']
    # checking if user entered all the fields or not
    if user_id and kid_name and kid_age and parent_phone and parent_email:
        if len(parent_phone) != 10:
            messages.error(request, 'Invalid phone number')
            return redirect('home')
        else:

            child_info = child(user_id=request.user, name=kid_name, age=kid_age,
                               parent_contact_number=parent_phone, parent_email=parent_email)
            # saving the data to the database
            child_info.save()
            # displaying success message to the user and redirecting to home page
            messages.success(request, 'Child added successfully')
            return redirect('home')
    else:
        messages.error(request, 'Please fill all the fields')
        return redirect('home')

# edit meal page for editing the meal of the current kid


@login_required
def edit_meal_info(request, id):
    meal_info = kid_meal.objects.get(id=id)
    if request.method == 'GET':
        return render(request, 'pages/edit_meal_info.html', {'meal_info': meal_info})
    if request.method == 'POST':
        kid = meal_info.kid_id.id

        img_url = request.POST['img_url']
        food_group = request.POST['food_group']

        if img_url and food_group:
            # checking if food group is defined or not
            is_approved = food_group != 'Unknown'
            # updating the meal info in the database
            kid_meal.objects.filter(id=id).update(
                image_url=img_url, food_group=food_group, updated_on=datetime.datetime.now(), is_approved=is_approved)
            messages.success(request, 'Meal info updated successfully')

            if food_group == 'Unknown':
                try:
                    # sending mail to the parent of the kid if food group is unknwon
                    send_mail(
                        'meal not approved',
                        'Hi,\n\nYour meal is not approved by the admin because food group is unknown.\nPlease check meal at - '+img_url,
                        settings.DEFAULT_FROM_EMAIL,
                        [meal_info.kid_id.parent_email],
                        fail_silently=False,
                    )
                except:
                    messages.error(request, 'Mail not sent')

            return redirect('kid_info', id=kid)
        else:
            messages.error(request, 'Please fill all the fields')
            return redirect('edit_meal_info', id=id)

# kid info page for displaying the details of the current kid


@login_required
def kid_info(request, id):
    if request.method == 'GET':
        kid_info = child.objects.get(id=id)
        meal_info = kid_meal.objects.filter(kid_id=id)

        return render(request, 'pages/kid_info.html', {'kid_id': id, 'kid_name': kid_info.name, 'kid_age': kid_info.age, 'parent_email': kid_info.parent_email, 'parent_phone': kid_info.parent_contact_number, 'meal_info': meal_info, 'current_user_name': request.user.first_name+' '+request.user.last_name})

# page for add meal info of the current kid


@login_required
def add_meal(request, id):
    meal_info = kid_meal.objects.get(id=id)
    kid = child.objects.get(id=id)

    img_url = request.POST['img_url']
    food_group = request.POST['food_group']

    if img_url and food_group:
        is_approved = food_group != 'Unknown'
        meal_info = kid_meal(kid_id=kid, image_url=img_url, food_group=food_group,
                             approved_by=request.user, is_approved=is_approved)
        meal_info.save()
        messages.success(request, 'Meal added successfully')

        if food_group == 'Unknown':
            try:
                # sending mail to the parent of the kid if food group is unknwon
                send_mail(
                    'meal not approved',
                    'Hi,\n\nYour meal is not approved by the admin because food group is unknown.\nPlease check meal at - '+img_url,
                    settings.DEFAULT_FROM_EMAIL,
                    [meal_info.kid_id.parent_email],
                    fail_silently=False,
                )
            except:
                messages.error(request, 'Mail not sent')

        return redirect('kid_info', id=id)
    else:
        messages.error(request, 'Please fill all the fields')
        return redirect('kid_info', id=id)

# route handler for deleting the meal of the current kid


@login_required
def delete_meal(request, id):
    kid_id = kid_meal.objects.get(id=id).kid_id.id
    kid_meal.objects.get(id=id).delete()
    messages.success(request, 'Meal deleted successfully')
    return redirect('kid_info', id=kid_id)

# route handler for editing the details of the current kid


@login_required
def edit_kid_info(request, id):
    kid_info = child.objects.get(id=id)
    kid_info.name = request.POST['kid_name']
    kid_info.age = request.POST['kid_age']
    kid_info.parent_email = request.POST['parent_email']
    kid_info.parent_contact_number = request.POST['parent_phone']
    if kid_info.name and kid_info.age and kid_info.parent_email and kid_info.parent_contact_number:
        kid_info.save()
        messages.success(request, 'Child updated successfully')
        return redirect('kid_info', id=id)
    else:
        messages.error(request, 'Please fill all the fields')
        return redirect('kid_info', id=id)

# route handler for deleting the current kid


@login_required
def delete_kid(request, id):
    if request.method == 'GET':
        child_info = child.objects.get(id=id)
        child_info.delete()
        messages.success(request, 'Child deleted successfully')
        return redirect('home')

# route handler registration page for registering new user


def signup(request):
    if request.method == 'POST':
        user_name = request.POST['user_name']
        user_email = request.POST['user_email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        user_password = request.POST['user_password']
        confirm_password = request.POST['confirm_password']
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
                messages.info(request, 'User created')
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


# route handler for logout of the current user

def logoutuser(request):
    logout(request)
    messages.success(request, 'Logged out Successfully')
    return redirect('home')

# route handler for login page for logging in the user


def loginuser(request):
    if request.method == 'GET':
        # checking if the user is already logged in or not and redirecting to home page if he is already logged in
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
