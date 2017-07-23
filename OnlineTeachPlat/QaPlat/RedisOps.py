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

    BIZ_RANK_INFLUENCE_FACTOR = "RankInfFactor"
    BIZ_RANK = "RANK"

    # 每个问题影响因素--使用哈希
    def getRankInfluencesKey(self,rankType,rankId):
        return self.BIZ_RANK_INFLUENCE_FACTOR + self.split + rankType + rankId

    # rankType: 1问题排名 
    # 使用有序集
    def getRankKey(self,rankType):
        return self.BIZ_RANK + self.split + rankType


    # 实体的关注列表
    def getFolloweeKey(self,entityType,entityId):
        return self.BIZ_FOLLOWEE + self.split + entityType + entityId

    # 实体的粉丝列表
    def getFollowerKey(self,entityType,entityId):
        return self.BIZ_FOLLOWER + self.split + entityType + entityId

    # 业务LIKE
    def getLikeKey(self, entityType, entityId):
        # print "get the like key"
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
            # 注意redis.py 实现zadd 的参数于redis 本身zadd 位置不同
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

class RedisHash(object):
    """docstring for Redis"""
    def __init__(self,rds=redis.Redis(connection_pool=pool)):
        super(RedisHash, self).__init__()
        self.r = rds

    def hset(self,key,field,value):
        try:
            self.r.hset(key,field,value)
            return True
        except Exception as e:
            print e
            return False

    def hget(self,key,field):
        try:
            return self.r.hget(key,field)
        except Exception as e:
            print e
            return False

    def hdel(self,key,field):
        try:
            self.r.hdel(key,field)
            return True
        except Exception as e:
            print e
            return False

    def hincrby(self,key,field,count):
        try:
            return self.r.hincrby(key,field,count)
        except Exception as e:
            print e
            return False

    def hvals(self,key):
        try:
            return self.r.hvals(key)
        except Exception as e:
            print e
            return False

    # values是一个字典
    def hmset(self,key,values):
        """
            values是一个字典
        """
        try:
            self.r.hmset(key,values)
            return True
        except Exception as e:
            print e
            return False

    def hmget(self,key,fields):
        """
            fields 是一个列表
        """
        try:
            return self.r.hmget(key,fields)
        except Exception as e:
            print e
            return False

    def hkeys(self,key):
        try:
            return self.r.hkeys(key)
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
