from django import urls
from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('loginuser/', views.loginuser, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logoutuser/', views.logoutuser, name='logout'),
    path('add-child/', views.add_child, name='child'),
    path('delete-kid/<int:id>', views.delete_kid, name='delete_kid'),
    path('edit-kid/<int:id>', views.edit_kid, name='edit_kid'),
]
