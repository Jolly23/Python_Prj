#coding=utf-8
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout

# Create your views here.
def index(request):
    username = 'jolly'
    return render(request,'accounts/index.html',{'username':username})

def register(request):
    '''注册视图'''
    if request.method == 'POST':
        #注册完毕，直接登陆
        return HttpResponseRedirect('/accounts/index')
    return render(request,'accounts/register.html')

def login(request):
    '''登陆'''
    template_var={}
    if request.method == 'POST':
        username = request.POST.get('username')
        template_var = {'error':'must register firstly!','username':username}
    return render(request,'accounts/login.html',template_var,)

def logout(request):
    return render(request,'accounts/logout.html',)

