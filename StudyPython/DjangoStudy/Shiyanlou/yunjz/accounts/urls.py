#coding=utf-8
from django.conf.urls import patterns,include,url
from django.contrib import admin
from accounts import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^index',views.index,name='index'),
    url(r'^login',views.login,name='login'),   
    url(r'^logout',views.logout,name='logout'),
    url(r'^register',views.register,name='register'),
)
