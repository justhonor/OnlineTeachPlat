# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from datetime import datetime  
class UserInfo(User):
	"""docstring for UserInfo"""
	
	def Get_all_users(self):
		users = User.objects.all()		
		return users

class ClassInfo(models.Model):
	"""docstring for ClassInfo"""
	CHOICES=(
		('p','通过'),
		('r','拒绝'),
		('w','等待'),
	)
	id = models.AutoField(primary_key=True)
	class_name = models.CharField(max_length=100)
	teacher_id = models.CharField(max_length=100,default=True)
	request_name = models.CharField(max_length=100)
	request_time = models.DateField(auto_now=True)
	status = models.CharField(max_length=4,default="等待",editable=False)

		