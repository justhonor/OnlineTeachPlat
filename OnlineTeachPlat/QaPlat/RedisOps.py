# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import redis

host = 'localhost'
port = 6379
db = 0

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)


class RedisKeyutil(object):
    """docstring for RedisKeyutil"""

    def __init__(self):
        super(RedisKeyutil, self).__init__()

    split = "_"
    # 业务名称
    BIZ_LIKE = "LIKE"
    BIZ_DISLIKE = "DISLIKE"
    BIZ_FOLLOWER = "FOLLOWER"
    BIZ_FOLLOWEE = "FOLLOWEE"

    # 实体的关注列表
    def getFolloweeKey(self,entityType,entityId):
        return self.BIZ_FOLLOWEE + self.split + entityType + entityId

    # 实体的粉丝列表
    def getFollowerKey(self,entityType,entityId):
        return self.BIZ_FOLLOWER + self.split + entityType + entityId

    # 业务LIKE
    def getLikeKey(self, entityType, entityId):
        print "get the like key"
        return self.BIZ_LIKE + self.split + entityType + entityId

    # 业务DISLIKE
    def getDisLikeKey(self, entityType, entityId):
        return self.BIZ_DISLIKE + self.split + entityType + entityId

class RedisZset(object):
    """docstring for RedisZset"""
    def __init__(self,rds=redis.Redis(connection_pool=pool)):
        super(RedisZset, self).__init__()
        self.r = rds

    def zadd(self,key,score,member):
        try:
            self.r.zadd(key,member,score)
            return True
        except Exception as e:
            print e
            return False

    def zrem(self, key, member):
        try:
            self.r.zrem(key,member)
            return True
        except Exception as e:
            print e
            return False

    def zcard(self,key):
        try:
            return self.r.zcard(key)
        except Exception as e:
            print e
            return False

    def zcount(self,key,Min,Max):
        try:
            self.r.zcount(key,Min,Max)
            return True
        except Exception as e:
            print e
            return False

    def zrevrange(self, key, start,stop):
        try:
            return self.r.zrevrange(key,start,stop)
        except Exception as e:
            print e
            return False

    def zrange(self, key, start,stop):
        try:
            return self.r.zrange(key,start,stop)
        except Exception as e:
            print e
            return False    

    def zscore(self,key,member):
        try:
            return self.r.zscore(key,member)
        except Exception as e:
            print e
            return False   


class RedisSet(object):
    """docstring for RedisSet"""

    def __init__(self):
        super(RedisSet, self).__init__()
    r = redis.Redis(connection_pool=pool)

    def sadd(self, key, value):
        try:
            self.r.sadd(key, value)
            return True
        except Exception as e:
        	print e
        	return False

    def srem(self, key, value):
    	try:
    		self.r.srem(key,value)
    		return True
    	except Exception as e:
    		print e
    		return False

    def sismember(self, key,value):
        try:
            return self.r.sismember(key,value)
        except Exception as e:
            print e
            return False

    def scard(self, key):
        try:
            return self.r.scard(key)
        except Exception as e:
            print e
            return False
