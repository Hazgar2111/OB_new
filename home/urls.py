from django.urls import include, re_path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

app_name = 'home'
urlpatterns = [
    re_path(r'^', views.index, name='index'),
    #re_path(r'^$', views.index, name='index'),

]

urlpatterns += staticfiles_urlpatterns()
