# -*- coding: utf-8 -*-
from django.shortcuts import render
# Create your views here.

def home(request):
    List = map(str, range(100))# 一个长度为100的 List
    return render(request, 'home.html', {'List': List})


