from datetime import datetime, timedelta
from django.conf import settings
from django.contrib import auth
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class ExceptionMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        return HttpResponse("in exception")


class AutoLogout:
    def process_request(self,request):
        if not request.user.is_authenticated():
            # Can't log out if not logged in
            return redirect('home:index')

        try:
            if datetime.now() - request.session['last_touch'] > timedelta(0, settings.AUTO_LOGOUT_DELAY * 60, 0):
                auth.logout(request)
                del request.session['last_touch']
                return redirect('home:index')
        except KeyError:
            pass

        request.session['last_touch'] = datetime.now()
