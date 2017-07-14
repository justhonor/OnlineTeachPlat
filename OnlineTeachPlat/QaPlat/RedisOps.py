# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import redis

host = 'localhost'
port = 6379
db = 0

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)

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
