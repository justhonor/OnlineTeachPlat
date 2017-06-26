# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class UserInfo(User):
	"""docstring for UserInfo"""
	
	def Get_all_users(self):
		users = User.objects.all()		
		return users



