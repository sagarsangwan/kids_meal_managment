from django import urls
from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('loginuser/', views.loginuser, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logoutuser/', views.logoutuser, name='logout'),
    path('add-kid/', views.add_child, name='kid'),
    path('delete-kid/<int:id>', views.delete_kid, name='delete_kid'),
    path('kid-info/<int:id>', views.kid_info, name='kid_info'),
    path('edit-kid-info/<int:id>', views.edit_kid_info, name='edit_kid_info'),
    path('add-meal/<int:id>', views.add_meal, name='add_meal'),
    path('edit-meal-info/<int:id>', views.edit_meal_info, name='edit_meal'),
    path('delete-meal/<int:id>', views.delete_meal, name='delete_meal'),
]
