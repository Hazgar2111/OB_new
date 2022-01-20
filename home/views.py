from django.shortcuts import render
from django.http import HttpResponse
from sign_in.models import LoginValue
from django.http import HttpResponse
from sign_in.models import Cards


def index(request):
    return render(request, 'home/homePage.html')











