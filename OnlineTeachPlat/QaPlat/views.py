# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

from django.views.decorators.csrf import csrf_exempt
import os

from django.contrib.auth.models import User, Group
from QaPlat.models import Question, Comment,Message
from QaPlat.SensitiveService import SensitiveService as Sservice

from django.db import connection
from LikeService import LikeService

from async.Event import EventType,EventModle,eventProducer,eventComsumer,ComsumerThread

# 开启异步事件处理线程
t = ComsumerThread()
t.start()

# 使用原生SQL
def SQL(sql):
    # 获得游标
    cursor=connection.cursor()
    
    # 执行sql
    cursor.execute(sql)
    
    # 取结果 
    results = cursor.fetchall()

    cursor.close()
    return results


# Create your views here.
class viewObject(object):
    """前端显示所需数据集合"""

    def setKey(self, key, value):
        self.__setattr__(key, value)

    def getKey(self, key):
        return self.__getattribute__(key)

# 赞踩服务
# like:1 喜欢 -1 不喜欢
@csrf_exempt
def likeService(request):


    entity_type  = request.POST.get("entity_type")
    entity_id = request.POST.get("entity_id")
    like = request.POST.get("like")
    userId = request.user.id

    # 评论的实体ID type:1 问题 2评论 
    if entity_type == "1": 
        entityOwnerId = Question.objects.get(id=entity_id).user_id
    elif entity_type == "2":
        entityOwnerId = Comment.objects.get(id=entity_id).user_id

    # import pdb; pdb.set_trace()
    l = LikeService()
    if like == "1":
        l.like(userId,entity_type,entity_id)
        # 触发异步事件
        em =  EventModle()
        em.setKey("TYPE","like").setKey("actorId",userId).setKey("entityType",entity_type)\
        .setKey("entityId",entity_id).setKey("entityOwnerId",entityOwnerId)
        producer = eventProducer()
        producer.fireEvnet(em)
    elif like == "-1":
        l.disLike(userId,entity_type,entity_id)
    counts = l.getLikecount(entity_type,entity_id)

    return HttpResponse(content=counts)

@csrf_exempt
def message(request):

    if request.method == "POST":
        # 发私信
        if request.POST.get('type') == "sendM":
            friendName = request.POST.get('friendName')
            
            fromid = request.user.id
            toid = User.objects.get(username=friendName).id
            content = request.POST.get("content")
            if toid < fromid:
                conversation_id="%s%s"%(toid,fromid)
            else:
                conversation_id="%s%s"%(toid,fromid)
            
            msg = Message.objects.create(fromid=fromid,toid=toid,content=content,conversation_id=conversation_id)
            return HttpResponse(content="success")
        elif request.POST.get('type') == "conversationMsg":
            # import pdb; pdb.set_trace()
            friendId = request.POST.get('friendId')
            if request.user.id < friendId:
                conversation_id = "%s%s"%(request.user.id,friendId)
            else:
                conversation_id = "%s%s"%(friendId,request.user.id)

            friendName = User.objects.get(id=friendId).username
            name = {
                "friendName":friendName,
            }
            cns = Message.objects.filter(conversation_id=conversation_id)
            return render(request,"QaPlat/conversation.html",{"myMsgs":cns,"friendName":name})



    # 每位朋友最新发来的信息
    my = []
    myMsgs = Message.objects.filter(toid=request.user.id).order_by('id').reverse()

    Sql = "select * from (select *  from QaPlat_message where toid='%s' order by id desc) as rever group by fromid;"%request.user.id 
    # 
    results = SQL(Sql)
    # import pdb; pdb.set_trace()
    for re in results:
        msgView = viewObject()
        fromid = re[1]
        friendName = User.objects.get(id=fromid).username

        # python manage.py dbinspect 查看表名及字段位置
        msgView.setKey("fromid",re[1])
        msgView.setKey("friendName",friendName)
        msgView.setKey("createdate",re[5])
        msgView.setKey("content",re[4])
        msgView.setKey("hasRead",re[6])

        my.append(msgView)
        

    # for myMsg in myMsgs:
    #     msgView = viewObject()
    #     friendName = User.objects.get(id=myMsg.fromid).username

    #     msgView.setKey("friendName",friendName)
    #     msgView.setKey("createdate",myMsg.create_date)
    #     msgView.setKey("content",myMsg.content)
    #     msgView.setKey("hasRead",myMsg.has_read)
    #     msgView.setKey("fromid",myMsg.fromid)

    #     my.append(msgView)
    return render(request,"QaPlat/message.html",{"myMsgs":my})


@csrf_exempt
def publicQ(request):
    if request.method == 'POST':
        # public question
        if request.POST.get('type') == "public":
            status, log = publicS(request)
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
        title = Sensitive.filter(request.POST.get('title'))
        content = Sensitive.filter(request.POST.get('content'))
        # title = request.POST.get('title')
        # content = request.POST.get("content")
        userId = request.user.id
        # import pdb; pdb.set_trace()
        question = Question.objects.create(
            title=title, content=content, user_id=userId)
        return True, "success"
    except Exception as e:
        return False, e


def qaPlat(request):
    # 显示最新问题
    questions = Question.objects.order_by('id').reverse()

    # 喜欢改问题的人数
    l = LikeService()
    news = []
    for qa in questions:
        if qa.title == "" or qa.user_id == "":
            continue
        username = User.objects.get(id=qa.user_id).username
        counts=l.getLikecount("1",str(qa.id))
        newQuestion = viewObject()
        newQuestion.setKey("title", qa.title)
        newQuestion.setKey("content", qa.content)
        newQuestion.setKey("date", qa.create_date)
        newQuestion.setKey("username", username)
        newQuestion.setKey("id", qa.id)
        newQuestion.setKey("type","1")
        newQuestion.setKey("likeCount",counts)
        news.append(newQuestion)

    return render(request, "QaPlat/qa.html", {'news': news})


@csrf_exempt
def oneQuestion(request):

    # 显示该问题
    qId = request.POST.get("questionId")
    qa = Question.objects.get(id=qId)
    # import pdb; pdb.set_trace()
    username = User.objects.get(id=qa.user_id).username
    newQuestion = viewObject()
    newQuestion.setKey("title", qa.title)
    newQuestion.setKey("content", qa.content)
    newQuestion.setKey("date", qa.create_date)
    newQuestion.setKey("username", username)
    newQuestion.setKey("type","1")
    newQuestion.setKey("id", qa.id)

    # 喜欢问题
    l = LikeService()
    # 显示问题评论
    comt=[]
    comments = Comment.objects.filter(entity_id=qId)
    # import pdb; pdb.set_trace()
    for com in comments:
        comView = viewObject()
        counts = l.getLikecount("2",str(com.id))
        commentUser = User.objects.get(id=com.user_id)
        comView.setKey("content",com.content)
        comView.setKey("create_date",com.create_date)
        comView.setKey("commentUser",commentUser)
        comView.setKey("commentId",com.id)
        comView.setKey("type","2")
        comView.setKey("likeCount",counts)
        comt.append(comView)


    return render(request, "QaPlat/oneQa.html", {'news': newQuestion,'comments':comt})


@csrf_exempt
def commentSubmit(request):

    comment = request.POST.get("comment")
    entity_type = request.POST.get("entity_type")
    entity_id = request.POST.get("entity_id")
    user_id = request.user.id
    

    com = Comment.objects.create()
    com.content = comment
    com.user_id = user_id
    com.entity_type = entity_type
    com.entity_id = entity_id   
    com.save()
    return HttpResponse(content="yes")


def index(request):
    return render(request, "QaPlat/qa.html")


def login(request):
    pass


@csrf_exempt
def uploadFile(request):
    if request.method == "POST":    					# 请求方法为POST时，进行处理
        # 获取上传的文件，如果没有文件，则默认为None
        myFile = request.FILES.get("myfile", None)
        if not myFile:
            return HttpResponse("no files for upload!")
        destination = open(os.path.join(
            "/home/aiapple/OnlineTeachPlat/OnlineTeachPlat/QaPlat/zuoye", myFile.name), 'a+')    # 打开特定的文件进行二进制的写操作
        for chunk in myFile.chunks():      				# 分块写入文件
            destination.write(chunk)
        destination.close()
        return HttpResponse("upload over!")
