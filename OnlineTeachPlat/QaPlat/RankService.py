# -*- coding: utf-8 -*-
from RedisOps import RedisSet,RedisKeyutil,RedisHash,RedisZset
import math

class RankService(object):
	"""
		rank 通用服务
		使用ZSET 根据socre排序
		使用HSET 存储计算socre所需信息

	"""
	def __init__(self):
		super(RankService, self).__init__()

	def getRankKey(self,rankType):
		return RedisKeyutil().getRankKey(rankType)

	def setRankScore(self,rankType,rankId,score):
		rankKey = self.getRankKey(rankType)
		RS = RedisZset()
		# print "rankKey:%s type score:%s score:%s"%(rankKey,type(score),score)
		try:
			RS.zadd(rankKey,score,rankId)
			return True
		except Exception as e:
			print e
			return False

	# 返回排序结果
	def getRankResult(self,rankType,offset=0,count=-1):
		rankKey = self.getRankKey(rankType)
		RS = RedisZset()
		try:
			return RS.zrevrange(rankKey,offset,count)
		except Exception as e:
			print e
			return False

	def  getRankInfluencesKey(self,rankType,rankId):
		return RedisKeyutil().getRankInfluencesKey(rankType,rankId)

	def setInfluenceFactors(self,rankType,rankId,factors):
		"""
			设置及更新Rank影响因素的值
			factors需是字典
		"""
		RankIKey = self.getRankInfluencesKey(rankType,rankId)
		RH = RedisHash()
		try:
			RH.hmset(RankIKey,factors)
			print "设置及更新Rank影响因素的值"
			return True
		except Exception as e:
			print e
			return False

	def getInfluenceFactors(self,rankType,rankId):
		"""
			拿到改rank的所有影响因素
		"""
		RankInflKey = self.getRankInfluencesKey(rankType,rankId)
		RH = RedisHash()
		try:
			return RH.hkeys(RankInflKey)
		except Exception as e:
			print e
			return False

	def getFactorsValue(self,rankType,rankId,factors):
		"""
			factors --> 列表
			拿到影响因素值
		"""
		RankInflKey = self.getRankInfluencesKey(rankType,rankId)
		RH = RedisHash()
		try:
			return RH.hmget(RankInflKey,factors)
		except Exception as e:
			print e
			return False

	def CalculatQuestionScores(self,rankType,rankId):
		"""
			计算问题rank值
			影响因素:

						* Qviews:问题浏览数，通过log来平滑
						* Qanswer:问题回答数，有回答的题目才是好问题
						* Qscore:问题赞踩差，赞的越多，问题越好
						* sum(Ascores):回答赞踩差，回答的越多问题越好
						* QageInHours:题目发布到现在的时间差，时间越久排名越后
						* Qupdated:最新的回答时间到现在的时间差，越新关注度越高。
			
			公式: score = L / R
				正向因子 L:
							(log(Qviews)*4) + ((Qanswer*Qscore)/5) + sumAscores
				负向因子 R:
							((QageInHours+1)) - ((QageInHours - Qupdated)/2)^1.5
		"""
		# 判断影响因素名称是否正确
		Getfactors = self.getInfluenceFactors(rankType,rankId)
		factors = [
			'Qviews','Qanswer','Qscore','sumAscores','QageInHours','Qupdated'
		]
		for Gf in Getfactors:
			if Gf not in factors:
				print "rankType:%s 因素设置错误"%rankType
				return -1

		values = self.getFactorsValue(rankType,rankId,factors)
		# 判断是否正确设置
		# print "CQ getFV:%s ,type values:%s"%(values,type(values))
		if isinstance(values,list):
			if None in values:
				print "有因素值没有设置"
				return -100
		else:
			print "GetFactorsValue error!"
			return -300

		L = ( math.log( int(values[0]) ) * 4.0 ) + (( int(values[1]) * int(values[2]) )/5.0)\
		 + int(values[3])

		R = ( int(values[4]) + 1.0 ) - math.pow( ( int(values[4]) - int(values[5]) ) / 2.0 , 1.1)
		score = L / R 

		return score

	def CalculateAndUpdate(self,rankType,rankId):
		"""
			计算并更新Rank值
			rankType rankId 确定每个实体rank
		"""
		if rankType == "QuestionRank" or rankType == "TRank":
			try:
				# 计算
				score = self.CalculatQuestionScores(rankType,rankId)
				print "Calculate score:%s"%score
			except Exception as e:
				print e
				return False			
			
			try:
				# 更新Scores
				self.setRankScore(rankType,rankId,score)
				print "更新Scores"
				return True
			except Exception as e:
				print e
				return False

		return -1



		
