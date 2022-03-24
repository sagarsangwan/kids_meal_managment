from django import urls
from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home')
]
