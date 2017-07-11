# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.
# from QaPlat.SensitiveService import TrieNode
from SensitiveService import  SensitiveService as SS
import os 
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


text='你好色 情吧'
text='你好*色*情*我们吧'
# c1 = "."
# c2 = " "
# c3 = "*"
# c4 = "##"

# cm  = [" ",".","*","#","你","n"]
# text='你好赌博吧到沙发'

s = SS()
print s.filter(text)
# text
# for uchar in cm:
# 	# import pdb; pdb.set_trace()
# 	print "type:%s uchar:%s ord:%s "%(type(uchar),uchar,ord(uchar))
# 	s.isSymbol(uchar)




# print s.filter(text)
# nd = TrieNode()
# root = TrieNode()
# nd.Init(root)
# print "this is root :",root.subNodes.items()

# f = open("Sensitive.txt",'r+')
# words=f.readlines()
# # 
# i = 1 
# for word in words:
	
# 	word.rstrip()
# 	wDecode = word.decode('utf-8')
	
# 	import pdb; pdb.set_trace()
# 	print wDecode
# f.close()
# 	# 汉字列表
# 	start = 0
# 	end = 0
# 	hanzi = []
# 	print "word:",word
# 	while ( end < len(word)):
# 		end = end +3
# 		hanzi.append(word[start:end])
# 		start = end
# 		# import pdb; pdb.set_trace()	 
# 	for i in hanzi: 
# 		print i

# 	# self.addWord(word.rstrip(),rootNode)
# f.close()



# class t(object):
# 	"""docstring for t"""
# 	def __init__(self):
# 		super(t, self).__init__()

# t1 = t()
# print  "t1 id :%s"%id(t1)
# t1 = t()
# print  "t1 id :%s"%id(t1)