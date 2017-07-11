# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import copy

# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

class TrieNode(object):
		"""前缀树"""
		def __init__(self):
			super(TrieNode,self).__init__()
			# 当前节点下所有的子节点 ab ac ad
			# a 下面就有 b c d 三个子节点
			self.subNodes = {}
			# 标记敏感词的结尾
			self.end = False

		# 初始化前缀
		# from QaPlat.SensitiveService import TrieNode as tn
		def Init(self,rootNode):
			# import pdb; pdb.set_trace()
			f = open("/home/aiapple/OnlineTeachPlat/OnlineTeachPlat/QaPlat/Sensitive.txt",'r+')
			words=f.readlines()
			for word in words:

				# 转换成unicode对象
				wDecode = word.decode('utf-8')
				self.addWord(wDecode,rootNode)

			f.close()

		def addWord(self,Dword,rootNode):
			tempNode = TrieNode()
			tempNode = rootNode
			word = Dword.rstrip('\n')
			# word = Dword.rsrtip('\n')
			# import pdb; pdb.set_trace()
			# print "tempNode id = %s"%id(tempNode)
			# print "rootNode %s"%id(rootNode)
			for i in range(len(word)):
				# import pdb; pdb.set_trace()
				cc = word[i]
				node = TrieNode()
				# print "the key is :%s"%cc
				# print "i=%s nodeid=%s"%(i,id(node))

				# 拿到字节点
				if tempNode.subNodes.has_key(cc):
					node.subNodes=tempNode.subNodes[cc]
				else:
					# print "new nodeid=%s  newnodeSub:%s"%(id(node),node.subNodes)
					tempNode.addSubNode(cc,node)
					# print "rootNode sub:%s"%rootNode.subNodes
				
				tempNode = node
				# print "=====node:",node
				# print "tempNode:",tempNode
				# print "====node is tempNode",(node is tempNode)


				# tempNode = copy.deepcopy(node)
				# print "node:",node
				# print "tempNode:",tempNode
				# print "node is tempNode",(node is tempNode)
				# print "new tempNodeId=%s tempsub:%s"%(id(tempNode),tempNode.subNodes)
				# print "after for i rootNode subnodes%s"%rootNode.subNodes
				# 敏感词尾加标记
				if i == len(word)-1:
					tempNode.setkeywordEnd()
					# print "is end now rootnode:%s"%rootNode.subNodes
				
		def addSubNode(self,key,Node):
			self.subNodes[key] = Node.subNodes
			
		def isKeyWordEnd(self): 
			if self.end == True:
				return True
			else:
				return False

		def setkeywordEnd(self): 
			self.end = True
			self.subNodes["_end_"] = "end"

class SensitiveService(TrieNode):
	"""敏感词过滤"""
	def __init__(self):
		super(SensitiveService, self).__init__()

		# 初始化敏感词
		try:
			# import pdb; pdb.set_trace()
			self.nd = TrieNode()
			self.root = TrieNode()
			self.nd.Init(self.root)
			print "敏感词前缀树:%s"%self.root.subNodes
		except Exception as e:
			print "初始化敏感词失败"

	def filter(self,text):

		replacement = "***"
		result = ""
		OneWord= ""
		rootNode = self.root
		begin = 0 
		position = 0

		tempNode = {}
		tempNode = rootNode.subNodes
		print "len text",len(text)
		while (position < len(text)):
			han = text[position]
			# import pdb; pdb.set_trace()
			# print "汉字  %s"%han
			if tempNode.has_key(han):
				print "前缀中有该字:%s 前缀树:%s "%(han,tempNode)
				if tempNode[han].has_key('_end_'):
					# 发现敏感词
					print "发现敏感词:%s begin:%s postion:%s "%(text[begin:position+1],begin,position)
					
					result = result + replacement
					position = position + 1
					begin = position
					tempNode = rootNode.subNodes
					OneWord = ""
				else:
					# 继续查找
					print "在前缀树中发现某个字,在其子树中继续查找 begin:%s postion:%s"%(begin,position)
					position = position + 1
					OneWord = OneWord + han
					# 查到某个开头,则在其子节点中继续查找
					tempNode = tempNode[han]
					print "子树:%s"%tempNode 
			else:
					if position == begin:
						print "前缀中没有该字:%s begin:%s position:%s"%(han,begin,position)
						result = result + OneWord+ han
					position = begin + 1
					begin = position
					tempNode = rootNode.subNodes
					OneWord = ""
					# print "tempNode",tempNode
					# print "rootNode.sub",rootNode.subNodes

		# 将最后过滤的字加上
		# result = result + han
		return  result


