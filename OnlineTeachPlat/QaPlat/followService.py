# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from RedisOps import RedisSet,RedisKeyutil,RedisZset
import datetime
RedisKeyutil = RedisKeyutil()
class FollowService(object):
	"""关注通用服务"""
	def __init__(self):
		super(FollowService, self).__init__()

	def follow(self,entityType,entityId,userId,userType='3'):
		# 实体的粉丝列表
		followerKey = RedisKeyutil.getFollowerKey(entityType,entityId)
		print "followerKey:%s enType:%s enId:%s uId:%s uType:%s"%(followerKey,entityType,entityId,userId,userType)

		# 用户的关注列表,定义userType:3
		followeeKey = RedisKeyutil.getFolloweeKey(userId,userType)
		print "followeeKey:%s enType:%s enId:%s uId:%s uType:%s"%(followeeKey,entityType,entityId,userId,userType)

		date = int(datetime.date.today().strftime("%Y%m%d"))
		import pdb; pdb.set_trace()
		try:
			split = "_"
			instance = entityType + split + entityId
			rz = RedisZset()
			rz.zadd(followerKey,date,userId)
			rz.zadd(followeeKey,date,instance)
			return True
		except Exception as e:
			print e
			return False

	def unfollow(self,entityType,entityId,userId,userType='3'):
		followerKey = RedisKeyutil.getFollowerKey(entityType,entityId)
		followeeKey = RedisKeyutil.getFolloweeKey(userId,userType)
		# import pdb; pdb.set_trace()
		try:
			split = "_"
			instance = entityType + split + entityId
			rz = RedisZset()
			rz.zrem(followerKey,userId)
			rz.zrem(followeeKey,instance)
			return True
		except Exception as e:
			print e
			return False

	# 实体对象的粉丝
	def getFollowers(self,entityType,entityId,offset,count):
		followerKey = RedisKeyutil.getFollowerKey(entityType,entityId)
		try:
			rz = RedisZset()
			return rz.zrevrange(followerKey,offset,count)
		except Exception as e:
			print e
			return False

	# 实体对象的关注列表
	def getFollowees(self,entityType,entityId,offset,count):
		followeeKey = RedisKeyutil.getFollowerKey(entityType,entityId)
		try:
			rz = RedisZset()
			return rz.zrevrange(followeeKey,offset,count)
		except Exception as e:
			print e
			return False

	def getFollowersCount(self,entityType,entityId):
		followerKey = RedisKeyutil.getFollowerKey(entityType,entityId)
		rz = RedisZset()
		return rz.zcard(followerKey)

	def getFolloweesCount(self,entityType,entityId):
		followeeKey = RedisKeyutil.getFollowerKey(entityType,entityId)
		rz = RedisZset()
		return rz.zcard(followeeKey)

	def isFollower(self,entityType,entityId,userId):
		followerKey = RedisKeyutil.getFollowerKey(entityType,entityId)
		rz = RedisZset()
		return rz.zscore(followerKey,userId) != None





