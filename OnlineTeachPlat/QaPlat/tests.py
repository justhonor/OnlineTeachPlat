# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# from LikeService import LikeService
# from async.Event import EventType,EventModle,eventProducer,eventComsumer,workThread

from Queue import Queue
from threading import Thread as thread
import os,time

from RedisOps import RedisZset,RedisHash
from RankService import RankService

import redis

host = 'localhost'
port = 6379
db = 0
s = 'sdf'
print type(s)
# pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
# rds=redis.Redis(connection_pool=pool)
factors1 = {
	 "Qviews":'10',
	 "Qanswer":"2",
	 "Qscore":'2',
	 "sumAscores":'3',
	 "QageInHours":'100',
	 "Qupdated":'50',
}
factors2 = {
	 "Qviews":'15',
	 "Qanswer":"3",
	 "Qscore":'4',
	 "sumAscores":'5',
	 "QageInHours":'100',
	 "Qupdated":'50',
}

factors3 = {
	 "Qviews":'10',
	 "Qanswer":"20",
	 "Qscore":'14',
	 "sumAscores":'3',
	 "QageInHours":'80',
	 "Qupdated":'50',
}
factors4 = {
	 "Qviews":'10',
	 "Qanswer":"2",
	 "Qscore":'2',
	 "sumAscores":'3',
	 "QageInHours":'80',
	 "Qupdated":'50',
}

rankType = "TRank"
rs = RankService()
print rs.IncrbyFactor(rankType,"qId10","Qviews")
print rs.getRankResult(rankType)
# 
# rs.setRankScore(rankType,11,"qId11")
# rs.setRankScore(rankType,12,"qId12")

# # print "所有Rank Id:",rs.getRankResult(rankType)
# # print "offset 0 count 2 Rank Id:",rs.getRankResult(rankType,0,2)
# # print "++++++++++++++++++++++++++++++++++++++"
# rs.setInfluenceFactors(rankType,"qId10",factors1)
# factors = rs.getInfluenceFactors(rankType,"qId10")
# # print "get Factors:",factors
# # rs.getFactorsValue(rankType,"qId10",factors)
# score = rs.CalculatQuestionScores(rankType,"qId10")
# rs.setRankScore(rankType,score,"qId10")
# print "====qId10==score:%s"%score

# rs.setInfluenceFactors(rankType,"qId11",factors2)
# factors = rs.getInfluenceFactors(rankType,"qId11")
# # print "get Factors:",factors
# rs.getFactorsValue(rankType,"qId11",factors)
# score = rs.CalculatQuestionScores(rankType,"qId11")
# rs.setRankScore(rankType,score,"qId11")
# print "====qId11==score:%s"%score

# rs.setInfluenceFactors(rankType,"qId12",factors3)
# factors = rs.getInfluenceFactors(rankType,"qId12")
# # print "get Factors:",factors
# rs.getFactorsValue(rankType,"qId12",factors)
# score = rs.CalculatQuestionScores(rankType,"qId12")
# rs.setRankScore(rankType,score,"qId12")
# print "====qId12==score:%s"%score

# rs.setInfluenceFactors(rankType,"qId13",factors4)
# factors = rs.getInfluenceFactors(rankType,"qId13")
# # print "get Factors:",factors
# rs.getFactorsValue(rankType,"qId13",factors)
# score = rs.CalculatQuestionScores(rankType,"qId13")
# rs.setRankScore(rankType,score,"qId13")
# print "====qId13==score:%s"%score


# print rs.getRankResult(rankType)
# print "++++++++++++++++++++++++++++++++++++++++"

# factors5 = {
#      "Qviews":'1',
#      "Qanswer":"0",
#      "Qscore":'1',
#      "sumAscores":'0',
#      "QageInHours":'1',
#      "Qupdated":'0',
# }

# print factors5
# print factors5

# rs.setInfluenceFactors(rankType,"qId1",factors5)
# print rs.CalculatQuestionScores(rankType,"qId1")
# rs.CalculateAndUpdate(rankType,"qId1")
# print rs.getRankResult(rankType)

# rs.setRankScore(rankType,score,"qId10")
# d = {}
# d.items
# r =  RedisHash()
# # r.hset("myhash","field",5)
# # print r.hget("myhash","field")
# # r.hset("myhash","field2",2)
# # r.hset("myhash","field3",3)
# # r.hdel("myhash","field2")
# # r.hincrby("myhash","field3",-1)
# # print  r.hvals("myhash")

# d={
# 	"user":"zhang2",
# 	"id":"2",
# }
# r.hmset("myhash",d)
# print  r.hvals("myhash")
# fie = ["user","id","vip","sdf",None]
# print r.hmget("myhash",fie)
# if None in fie:
# 	print "has none"
# # print r.hkeys("myhash")
# t = EventType()
# t.setVaule("like")

# a =  EventModle()
# a.setKey("TYPE",t.getValue()).setKey("actorId","123")\
# .setKey("entityType","1").setKey("entityId","798").setKey("entityOwnerId","159")
# print a.getKey("TYPE")

# b =  EventModle()
# b.setKey("TYPE","email").setKey("actorId","123")\
# .setKey("entityType","1").setKey("entityId","798").setKey("entityOwnerId","159")
# print b.getKey("TYPE")


# p = eventProducer()

# t = workThread()
# t.start()
# i = 0
# while True:
   
#     i = i + 1
#     print "test %s"%i
#     p.fireEvnet(b)
#     p.fireEvnet(a)
#     time.sleep(5)

# c = eventComsumer()
# c.get()
# print m.getKey("TYPE")
# print m.getKey("actorId")
# print m.getKey("entityOwnerId")