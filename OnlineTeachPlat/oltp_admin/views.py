# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
def index(request):
    '''主视图'''
    a={'app_path':'aaaa','form':{'username':{'label_tag':'input'}}}
    username = "Aiapple"

    return render(request, "base.html")

def login(request):
	pass

def logout(request):
	pass

def register(request):
	pass