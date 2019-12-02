from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import ListView, DetailView
from sign_in.models import LoginValue
app_name = 'sign_in'
urlpatterns = [
    url(r'^sign_up/', views.index_sign_up, name='index_sign_up'),
    url(r'^forgot_pass/', views.forgot_pass, name='forgot_pass'),
    path('new_user/', views.add_user, name='add_user'),
    path('recovery/', views.recovery_code, name='recovery_code'),
    path('new_pass/', views.new_pass, name='new_pass'),
    path('login_user/', views.login_user, name='login_user'),
    path('personal_cabinet/', views.personal_cabinet, name='personal_cabinet'),
    path('log_out/', views.logout1, name='log_out'),
    path('transfers/', views.transfers, name='transfers'),
    path('change_pass/', views.change_pass_index, name='change_pass_index'),
    path('change_pass1/', views.change_pass, name='change_pass'),
]
