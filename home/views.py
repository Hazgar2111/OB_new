from django.shortcuts import render
from django.http import HttpResponse
from sign_in.models import LoginValue
from django.http import HttpResponse
from sign_in.models import Cards


def index(request):
    return render(request, 'home/homePage.html')


def personal_cabinet(request):
    return render(request, 'home/personal_cabinet.html')


def index1(request):
    return render(request, 'home/test.html')








