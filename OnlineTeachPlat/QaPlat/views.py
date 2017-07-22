# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect, HttpResponse

from django.views.decorators.csrf import csrf_exempt
import os

from django.contrib.auth.models import User, Group
from QaPlat.models import Question, Comment,Message
from QaPlat.SensitiveService import SensitiveService as Sservice

from django.db import connection
from LikeService import LikeService

from async.Event import EventType,EventModle,eventProducer,eventComsumer,ComsumerThread

from followService import FollowService as Fs
import datetime
from RankService import RankService

# 开启异步事件处理线程
t = ComsumerThread()
t.start()

entityType={
    "question":'1',
    "comment":'2',
    "user":'3'
}

rankType ={
    # RankService.py 中使用到,作用范围未使用LEGB 的B 因此不可改 
    "question":"QuestionRank"
}



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

@csrf_exempt
def own(request):
    return render(request,"QaPlat/person.html")


@csrf_exempt
def person(request):
    print "========================================"
    # return HttpResponseRedirect('own')
    # import pdb; pdb.set_trace()
    userId = request.path.encode().split('/')[-2]

    
    InfoView = viewObject()
    InfoView.setKey("groupName",User.objects.get(id=userId).group_name)
    InfoView.setKey("userName",User.objects.get(id=userId).username)
    InfoView.setKey("userId",userId)
    InfoView.setKey("email",User.objects.get(id=userId).email)

    fs = Fs()
    IsFollow=fs.isFollower(entityType["user"],userId,request.user.id)
    InfoView.setKey("IsFollow",IsFollow)
    print "isfollow:",InfoView.IsFollow

    return render(request,"QaPlat/person.html",{"userInfo":InfoView})

@csrf_exempt
def profile(request):
    # 关注列表和粉丝类表给template
    entity_type = entityType["user"]
    entity_id = str(request.user.id)
    # 所有列表
    offset = 0 
    count = -1
    fs = Fs()
    followee=fs.getFollowees(entity_type,entity_id,offset,count)
    follower=fs.getFollowers(entity_type,entity_id,offset,count)

    # 可以关注问题,评论,用户
    fv = []
    for fee in followee:
        # entityTypeId[0]-->type  entityTypeId[1]-->id
        entityTypeId=fee.split("_")
        if entityTypeId[0] == "1":
            entity_type = entityTypeId[0]
            followerType = "关注问题"
            # print  "关注问题"
            # import pdb; pdb.set_trace()
            followerId = entityTypeId[1]
            title = Question.objects.get(id=int(entityTypeId[1])).title
            user_id = Question.objects.get(id=int(entityTypeId[1])).user_id
            username = User.objects.get(id=user_id).username
            # print "标题:%s 作者:%s "%(title,username)
        elif entityTypeId[0] == "2":
            entity_type = entityTypeId[0]
            followerType = "关注评论"
            followerId = entityTypeId[1]
            title = ""
            user_id = Comment.objects.get(id=int(entityTypeId[1])).user_id
            username = User.objects.get(id=user_id).username
            # print  "关注评论"
        elif entityTypeId[0] == "3":
            entity_type = entityTypeId[0]
            followerType = "关注用户"
            followerId = entityTypeId[1]
            title = ""
            username = User.objects.get(id=int(entityTypeId[1])).username
            # print  "关注用户"
        followeeView = viewObject()
        followeeView.setKey("followerType",followerType)
        followeeView.setKey("entityeType",entity_type)
        followeeView.setKey("followerId",followerId)
        followeeView.setKey("title",title)
        followeeView.setKey("username",username)
        fv.append(followeeView)

    # 粉丝是用户
    fl =[]
    for fer in follower:
        followerView=viewObject()
        followerView.setKey("userId",fer)
        followerView.setKey("username",User.objects.get(id=fer).username)
        # print "粉丝id:%s name:%s"%(followerView.username,followerView.userId)
        fl.append(followerView)

    return render(request,"QaPlat/profile.html",{"followees":fv,"followers":fl,"onwerName":request.user.username})

# 取消关注业务
@csrf_exempt
def unfollowS(request):
    entity_type  = request.POST.get("entity_type")
    entity_id = request.POST.get("entity_id")
    userId = str(request.user.id)
    # import pdb; pdb.set_trace()
    if entity_type is None or entity_id is None:
        return HttpResponse("wrong request \n type or id is None")
    else:
        fs = Fs()
        fs.unfollow(entity_type,entity_id,userId)
        return HttpResponse(content="d1")   
# followerKey:FOLLOWER_110 enType:1 enId:10 uId:57 uType:3
# followeeKey:FOLLOWEE_573 enType:1 enId:10 uId:57 uType:3

# 关注业务
@csrf_exempt
def followS(request):
    entity_type  = request.POST.get("entity_type")
    entity_id = request.POST.get("entity_id")
    userId = str(request.user.id)
    # import pdb; pdb.set_trace()
    if entity_type is None or entity_id is None:
        return HttpResponse("wrong request \n type or id is None")
    else:
        fs = Fs()
        fs.follow(entity_type,entity_id,userId)
        return HttpResponse(content="d1")   

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

    # Sql = "select * from (select *  from QaPlat_message where toid='%s' order by id desc) as rever group by fromid;"%request.user.id 
    Sql = "select *  from QaPlat_message where toid='69' group by fromid"
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
            # import pdb; pdb.set_trace()
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

    # 初始值
    QuestionFactors = {
         "Qviews":'1',
         "Qanswer":"0",
         "Qscore":'1',
         "sumAscores":'0',
         "QageInHours":'1',
         "Qupdated":'0',
    }
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

        import pdb; pdb.set_trace()
        qId = question.id
        # 问题发布成功设置其初始因素值
        try:
            rs = RankService()
            rs.setInfluenceFactors(rankType['question'].encode(),qId,QuestionFactors)
            rs.CalculateAndUpdate(rankType['question'].encode(),qId)
            return True, "success"
        except Exception as e:
            print e
            return False, e
    except Exception as e:
        return False, e


def qaPlat(request):

    # 我关注的问题
    # 关注列表和粉丝类表给template
    entity_type = entityType["user"]
    entity_id = str(request.user.id)
    # 所有列表
    offset = 0 
    count = -1
    fs = Fs()
    followee=fs.getFollowees(entity_type,entity_id,offset,count)

    # 可以关注问题,评论,用户
    fv = []
    for fee in followee:
        # entityTypeId[0]-->type  entityTypeId[1]-->id
        entityTypeId=fee.split("_")
        if entityTypeId[0] == "1":
            entity_type = entityTypeId[0]
            followerType = "关注问题"
            # print  "关注问题"
            # import pdb; pdb.set_trace()
            followerId = entityTypeId[1]
            title = Question.objects.get(id=int(entityTypeId[1])).title
            user_id = Question.objects.get(id=int(entityTypeId[1])).user_id
            username = User.objects.get(id=user_id).username
            # print "标题:%s 作者:%s "%(title,username)
        else:
            continue
        followeeView = viewObject()
        followeeView.setKey("followerType",followerType)
        followeeView.setKey("entityeType",entity_type)
        followeeView.setKey("followerId",followerId)
        followeeView.setKey("title",title)
        followeeView.setKey("username",username)
        fv.append(followeeView)    

    # 喜欢该问题的人数
    l = LikeService()

    # 显示最新问题
    questions = Question.objects.order_by('id').reverse()
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
        newQuestion.setKey("userId",qa.user_id)
        newQuestion.setKey("id", qa.id)
        newQuestion.setKey("type","1")
        newQuestion.setKey("likeCount",counts)
        news.append(newQuestion)
    # print news[0].title,news[0].content
    return render(request, "QaPlat/qa.html", {'news': news,"followerQa":fv})


@csrf_exempt
def oneQuestion(request):


    # 显示该问题
    # import pdb; pdb.set_trace()
    if request.method == "POST":
        qId = request.POST.get("questionId")
    # 用于我关注的问题
    elif request.method == "GET":
        qId = request.path.encode().split('/')[-2]
        
    qa = Question.objects.get(id=qId)
    # import pdb; pdb.set_trace()
    username = User.objects.get(id=qa.user_id).username
    newQuestion = viewObject()
    newQuestion.setKey("title", qa.title)
    newQuestion.setKey("content", qa.content)
    newQuestion.setKey("date", qa.create_date)
    newQuestion.setKey("username", username)
    newQuestion.setKey("userId",qa.user_id)
    newQuestion.setKey("type","1")
    newQuestion.setKey("id", qa.id)

    # 是否已关注
    fs = Fs()
    # import pdb; pdb.set_trace()
    IsFollow=fs.isFollower(entityType["question"],qId,request.user.id)
    newQuestion.setKey("IsFollow",IsFollow)

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
        comView.setKey("commentUserId",com.user_id)
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
