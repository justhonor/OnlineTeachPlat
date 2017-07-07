# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

from django.views.decorators.csrf import csrf_exempt
import os

from QaPlat.models import Question

# Create your views here.
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
        title = request.POST.get('title')
        content = request.POST.get("content")
        userId  = request.user.id
        # import pdb; pdb.set_trace()
        question = Question.objects.create(title=title,content=content,user_id=userId)
        return True,"success"
    except Exception as e:
        return False,e


def qaPlat(request):
    return render(request, "QaPlat/qa.html")

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

