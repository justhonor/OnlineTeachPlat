# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

from django.views.decorators.csrf import csrf_exempt
import os

from django.contrib.auth.models import User, Group
from QaPlat.models import Question
from QaPlat.SensitiveService import SensitiveService as Sservice

# Create your views here.

class viewObject(object):
    """前端显示所需数据集合"""
    def setKey(self,key,value):
        self.__setattr__(key,value)

    def getKey(self,key):
        return self.__getattribute__(key)


@csrf_exempt
def publicQ(request):
    if request.method == 'POST':
        # public question
        if request.POST.get('type') == "public":
            status,log = publicS(request)
            if status:
                return HttpResponse(content="success")
                # return HttpResponse(content="public question success")
            else:
                return HttpResponse(content="fail")
                # return HttpResponse(content="public question fail:%s"%log)
    return render(request, "QaPlat/publicQ.html") 

# save the question
def publicS(request):
    # import pdb; pdb.set_trace()
    try:
        # 敏感词过滤
        Sensitive = Sservice()
        # import pdb; pdb.set_trace()
        title =  Sensitive.filter(request.POST.get('title'))
        content = Sensitive.filter(request.POST.get('content'))
        # title = request.POST.get('title')
        # content = request.POST.get("content")
        userId  = request.user.id
        # import pdb; pdb.set_trace()
        question = Question.objects.create(title=title,content=content,user_id=userId)
        return True,"success"
    except Exception as e:
        return False,e


def qaPlat(request):
    # 显示最新问题
    questions =  Question.objects.order_by('id').reverse()

    news = []
    for qa in questions:
        if qa.title == "" or qa.user_id == "":
            continue
        username = User.objects.get(id=qa.user_id).username
        newQuestion = viewObject() 
        newQuestion.setKey("title",qa.title)
        newQuestion.setKey("content",qa.content)
        newQuestion.setKey("date",qa.create_date)
        newQuestion.setKey("username",username)
        news.append(newQuestion)

    return render(request, "QaPlat/qa.html",{'news':news})


def index(request):
	return render(request, "QaPlat/qa.html")
	
def login(request):
	pass

@csrf_exempt
def uploadFile(request):  
    if request.method == "POST":    					# 请求方法为POST时，进行处理  
        myFile =request.FILES.get("myfile", None)    	# 获取上传的文件，如果没有文件，则默认为None  
        if not myFile:  
            return HttpResponse("no files for upload!")  
        destination = open(os.path.join("/home/aiapple/OnlineTeachPlat/OnlineTeachPlat/QaPlat/zuoye",myFile.name),'a+')    # 打开特定的文件进行二进制的写操作  
        for chunk in myFile.chunks():      				# 分块写入文件  
            destination.write(chunk)  
        destination.close()  
        return HttpResponse("upload over!")  

