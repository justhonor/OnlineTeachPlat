# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from Queue import Queue
from threading import Thread as thread
import os,time
from django.contrib.auth.models import User, Group
from QaPlat.models import Question, Comment,Message
import copy

eventQ = Queue(maxsize=100)

Threads_numbers = 2

class EventType(object):
	"""docstring for EventType"""
	def __init__(self):
		super(EventType, self).__init__()
		self.eventType = {
			"like":0,
			"comment":1,
			"login":2,
			"email":3
		}
		self.typeValue=""

	def getValue(self):
		return self.typeValue

	def setVaule(self,value):
		try:
			if self.eventType.has_key(value):
				self.typeValue = value 
			else:
				raise  TypeError("worng type")
		except Exception as e:
			print e

class EventModle(object):
	"""事件发生现场"""
	def __init__(self):
		super(EventModle, self).__init__()
		TYPE = ""
		actorId = ""
		entityType = ""
		entityId = ""
		entityOwnerId = ""

	def setKey(self,key,value):
		self.__setattr__(key,value)
		return self

	def getKey(self,key):
		return self.__getattribute__(key)

class eventProducer(object):
	"""将事件push到队列"""
	def __init__(self):
		super(eventProducer, self).__init__()

	def fireEvnet(self,eventM):
		eventQ.put(eventM)
		print "queue len:%s",eventQ.qsize()


class likeHandler(object):
	"""like事件处理"""
	def __init__(self):
		super(likeHandler, self).__init__()

	def doHandler(self,em):
		# 发站内信
		print "发站内信"
		print em.entityOwnerId
		
        fromid = User.objects.get(username='admin')
        # toid = em.entityOwnerId
        # actorId = em.actorId
        # actorName = User.objects.get(id=actorId).username
        # content = "%s 给你点赞啦! entity_type=%s entity_id=%s "%(actorName,em.entityType,em.entityId)

        # if toid < fromid:
        #     conversation_id="%s%s"%(toid,fromid)
        # else:
        #     conversation_id="%s%s"%(toid,fromid)
        
        # # msg = Message.objects.create(fromid=fromid,toid=toid,content=content,conversation_id=conversation_id)

def dolikeHandler(em):
		# 发站内信
		print "发站内信"
		# print em.entityOwnerId
		fromid = str(User.objects.get(username='admin').id)
		toid = em.entityOwnerId
		actorId = em.actorId
		actorName = User.objects.get(id=actorId).username
		content = "%s 给你点赞啦! entity_type=%s entity_id=%s "%(actorName,em.entityType,em.entityId)
		
		if toid < fromid:
			conversation_id="%s%s"%(toid,fromid)
		else:
			conversation_id="%s%s"%(toid,fromid)
		# import pdb; pdb.set_trace()
		try:
			print("message create fromid:%s toid:%s content:%s conid:%s")%(fromid,toid,content,conversation_id)
			msg = Message.objects.create(fromid=fromid,toid=toid,content=content,conversation_id=conversation_id)
		except Exception as e:
			print e

class emailHandler(object):
	"""like事件处理"""
	def __init__(self):
		super(emailHandler, self).__init__()

	def doHandler(self):
		# 发站内信
		print "发站邮件"

class eventComsumer(object):
	"""从队列中拿事件并分发给相应处理函数"""
	def __init__(self):
		super(eventComsumer, self).__init__()


class ComsumerThread(thread):
	"""docstring for ComsumerThread"""
	def __init__(self):
		super(ComsumerThread, self).__init__()
		# threads = thread(target=get)
	def run(self):
		while True:
			# print "ComsumerThread run() thred id :%s",self.getName()
			# import pdb; pdb.set_trace()
			if not eventQ.empty():
				self.eventM = eventQ.get(block=False)
				if self.eventM.TYPE == "like":
					dolikeHandler(self.eventM)
					# likeH = likeHandler()
					# likeH.doHandler(self.eventM)
				elif self.eventM.TYPE == "email":
					emailHandler().doHandler()
				else:
					print "没有发现处理函数"
			time.sleep(1)


		

		
