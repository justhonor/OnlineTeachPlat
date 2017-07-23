# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from RedisOps import RedisSet,RedisKeyutil

class LikeService(object):
    """docstring for LikeService"""
    def __init__(self):
        super(LikeService, self).__init__()

    def like(self, userId, entityType, entityId):
        getKey = RedisKeyutil()
        redis = RedisSet()
        # 在该对象的喜欢集合中加上改用户
        likeKey = getKey.getLikeKey(entityType, entityId)
        redis.sadd(likeKey, userId)

        # 在该对象的不喜欢的集合中去除改对象
        dislikekey = getKey.getDisLikeKey(entityType, entityId)
        redis.srem(dislikekey, userId)
        return redis.scard(likeKey)

    def disLike(self, userId, entityType, entityId):
    	redis = RedisSet()
        getKey = RedisKeyutil()
        # 在该对象的喜欢集合中去除该用户
        likeKey = getKey.getLikeKey(entityType, entityId)
        redis.srem(likeKey, userId)

        # 在该对象的不喜欢的集合中增加该用户
        dislikekey = getKey.getDisLikeKey(entityType, entityId)
        redis.sadd(dislikekey, userId)
        return redis.scard(likeKey)

    def getLikeStatus(self,userId,entityType,entityId):
    	redis = RedisSet()
    	getKey = RedisKeyutil()
    	likeKey = getKey.getLikeKey(entityType,entityId)
    	dislikekey = getKey.getDisLikeKey(entityType,entityId)

    	# 喜欢1 不喜欢-1 无所谓0
    	if redis.sismember(likeKey,userId):
    		return "1"
    	elif redis.sismember(dislikekey,userId):
    		return "-1"
    	else:
    		return 0 

    def getLikecount(self,entityType,entityId):
    	redis = RedisSet()
    	getKey = RedisKeyutil()
    	likeKey = getKey.getLikeKey(entityType,entityId)

    	return redis.scard(likeKey)

