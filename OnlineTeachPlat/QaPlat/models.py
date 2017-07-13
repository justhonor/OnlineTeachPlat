# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
# 站内信
class Message(models.Model):
	"""docstring for ClassInfo"""
	id = models.AutoField(primary_key=True)
	fromid = models.CharField(max_length=10)
	toid = models.CharField(max_length=10)

	# 会话ID,toid_fromid or fromid_toid 两者较小的放在最前面
	conversation_id = models.CharField(max_length=10)
	content =  models.CharField(max_length=256)
	has_read = models.BooleanField(default=False)
	create_date = models.DateField(auto_now=True)

# 问题
class Question(models.Model):
	"""docstring for Question"""
	id = models.AutoField(primary_key=True)
	title = models.CharField(max_length=100)
	content =  models.TextField()
	user_id = models.CharField(max_length=10)
	create_date = models.DateField(auto_now=True)

# 评论
class Comment(models.Model):
	"""docstring for Comment"""
	id = models.AutoField(primary_key=True)
	content =  models.TextField()
	user_id = models.CharField(max_length=10)
	create_date = models.DateField(auto_now=True)

	# 评论的实体ID type:1 问题 2评论 
	entity_id = models.CharField(max_length=10)
	entity_type = models.CharField(max_length=1)
