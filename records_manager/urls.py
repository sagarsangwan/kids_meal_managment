from django import urls
from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('loginuser/', views.loginuser, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logoutuser/', views.logoutuser, name='logout'),
]
