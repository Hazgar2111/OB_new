from django.conf.urls import url, include
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

app_name = 'home'
urlpatterns = [
    url(r'^', views.index, name='index'),
    path('personal_cabinet/', views.personal_cabinet, name='personal_cabinet'),
    url(r'^$', views.index, name='index'),

]

urlpatterns += staticfiles_urlpatterns()
