# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from oltp_admin.form import RegisterForm

from oltp_admin.models import UserInfo,ClassInfo
from django.contrib.auth.models import User, Group
import pdb

from django.views.decorators.csrf import csrf_exempt

import simplejson as json 

# Create your views here.
# superuser root:root_11111 admin:admin_11111

# 每页显示10位用户
global PageUsers
PageUsers = 10

@csrf_exempt
def review(request):
        if request.method == 'POST' and request.POST.get("type") == "delete":
            class_ids = request.POST.get("class_ids")
            Class_ids = class_ids.split(',')[:-1]
            try:
                # import pdb; pdb.set_trace()
                for cid in Class_ids:
                    c = ClassInfo.objects.get(id=cid)
                    c.status = "拒绝"
                    c.save()
                return HttpResponse(content="delete class %s sucess" % (cid))
            except Exception as e:
                return HttpResponse(content="delete class %s failed" % (cid))

        elif request.method == 'POST' and request.POST.get("type") == "pass":
            class_ids = request.POST.get("class_ids")
            Class_ids = class_ids.split(',')[:-1]
            try:
                # import pdb; pdb.set_trace()
                for cid in Class_ids:
                    c = ClassInfo.objects.get(id=cid)
                    c.status = "通过"
                    c.save()
                return HttpResponse(content="pass class %s sucess" % (cid))
            except Exception as e:
                return HttpResponse(content="pass class %s failed" % (cid))
        else:
            Classes = ClassInfo.objects.all()
            return render(request, "oltp_admin/ClassReview.html",{'Classes':Classes})

def index(request):
    '''主视图'''
    # 登录则显示index页面
    # 未登录则重定向url = /oltp/login
    # pdb.set_trace()
    # User = UserInfo()
    # users = User.Get_all_users()

    LastUser = User.objects.last()
    LastUserId = LastUser.id
    users =  User.objects.filter(id__lte=LastUserId).order_by('id').reverse()[:PageUsers]

    if request.user.is_authenticated():
        if request.user.username == 'admin':
            # 管理用户
            return render(request, "oltp_admin/admin_index.html", {'users': users})
        else:
            # 普通用户
            # import pdb; pdb.set_trace()
            return render(request, "QaPlat/index.html")
    else:
        return HttpResponseRedirect("/oltp/login")


def logout(request):
    auth_logout(request)
    return render(request, "oltp_admin/logout.html")


def register(request):
    '''注册视图'''
    template_var = {}
    form = RegisterForm()

    if request.method == "POST":
        # 将表单提交的数据交给RegisterForm 进行验证
        # import pdb; pdb.set_trace()
        form = RegisterForm(request.POST.copy())
        
        if form.is_valid():
            # 验证通过，创建用户
            form.save()
            # 登录
            if _login(request, form.cleaned_data['username'], form.cleaned_data['password'], template_var):
                return render(request, "oltp_admin/index.html")

    template_var["form"] = form
    return render(request, "oltp_admin/register.html", template_var)


def login(request):
    '''登陆视图'''
    template_var = {}
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        if _login(request, username, password, template_var):
            try:
                tmp = request.GET['next']
                return HttpResponseRedirect(tmp)
            except:
                return HttpResponseRedirect("/oltp/")

        template_var.update({"username": username})

    return render(request, "oltp_admin/login.html", template_var)


def _login(request, username, password, dict_var):
    '''登陆核心方法'''
    ret = False
    # 验证用户
    # import pdb; pdb.set_trace()
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            ret = True
        else:
            dict_var["error"] = u'用户' + username + u'没有激活'
    else:
        dict_var["error"] = u'用户' + username + u'不存在或密码错误'
    return ret


@csrf_exempt
def admin(request):
    '''管理用户'''

    # type 值控制具体操作
    # 删除选中用户
    if request.method == 'POST' and request.POST.get("type") == "delete":
        usernames = request.POST.get("usernames")
        # import pdb; pdb.set_trace()
        Usernames = usernames.split(',')[:-1]
        for user in Usernames:
            print "delete ....%s" % (user)
            if del_user(request, user):
                print "delete %s sucess" % (user)
            else:
                return HttpResponse(content="delete %s failed" % (user))
        return HttpResponse(content="delete %s sucess" % (user))
    # 新增用户
    elif request.method == 'POST' and request.POST.get("type") == "add":
        if add_user(request):
            print "add %s sucess" % (request.POST.get("username"))
            return HttpResponse(content="Add %s sucess" % (request.POST.get("username")))
        else:
            return HttpResponse(content="add %s failed" % (request.POST.get("username")))
    # 修改用户信息
    elif request.method == 'POST' and request.POST.get("type") == "update":
        if update_user(request):
            print "update %s sucess" % (request.POST.get("username"))
            return HttpResponse(content="update %s sucess" % (request.POST.get("username")))
        else:
            return HttpResponse(content="update %s failed" % (request.POST.get("username")))
    # 查询用户信息
    elif request.method == 'POST' and request.POST.get("type") == "search":
        exist,userinfo  = search_user(request)
        # import pdb; pdb.set_trace()
        data = {}
        if exist:
            data = {
                "exist":"1",
                "username":userinfo.username,
                "email":userinfo.email,
                "group":userinfo.group_name,
                "status":userinfo.is_active
        }
            print "search %s sucess" % (request.POST.get("search_name"))
            return HttpResponse(content= json.dumps(data))
        else:
            data["exist"] = "0"
            return HttpResponse(content= json.dumps(data))  
    # 下一页
    elif request.method == 'POST' and request.POST.get("type") == "next":
        status,users = next_users(request)
        # import pdb; pdb.set_trace()
        if status and request.user.is_authenticated() and users.exists():
            if request.user.username == 'admin':
                # 管理用户
                return render(request, "oltp_admin/admin_index.html", {'users': users})
        else:
                # 没有更多用户
                return HttpResponseRedirect("/oltp/") 

    # 上一页
    elif request.method == 'POST' and request.POST.get("type") == "previous":
        status,users = previous_users(request)
        # import pdb; pdb.set_trace()
        if status and request.user.is_authenticated() and users.exists():
            if request.user.username == 'admin':
                # 管理用户
                return render(request, "oltp_admin/admin_index.html", {'users': users})
        else:
                # 没有更多用户
                return HttpResponseRedirect("/oltp/")  

def previous_users(request):
    try:
        FirstUser = request.POST.get("reference_user")
        FirstUserId = User.objects.filter(username=FirstUser).values("id")
        users =  User.objects.filter(id__gt=FirstUserId).order_by('id').reverse()[:PageUsers]
        return True,users
    except Exception as e:
        return False,e

def next_users(request):
    try:
        LastUser = request.POST.get("reference_user")
        LastUserId = User.objects.filter(username=LastUser).values("id")
        users =  User.objects.filter(id__lt=LastUserId).order_by('id').reverse()[:PageUsers]
        return True,users
    except Exception as e:
        return False,e

def search_user(request):
    try:
        username = request.POST.get("search_name")
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            return  True,user
        else:
            return False,"用户不存在"
    except Exception as e:
            return False,e


def update_user(request):
    # 需要对字段合法性验证
    # group -- 学生，教师，管理员
    # status -- True/False
    # username,email,password 的验证
    # 可在js中验证连带add_user()一起
    try:
        # import pdb; pdb.set_trace()
        username = request.POST.get("username") 
        user = User.objects.get(username=username)
        
        if request.POST.get("email"):
            user.email = request.POST.get("email")
        if request.POST.get("password"):
            # user.password = request.POST.get("password")
            # 使用加密算法加密存储密码
            user.set_password(request.POST.get("password"))
        if request.POST.get("group"):
            user.group_name = request.POST.get("group") 
        if request.POST.get("status"):
            user.is_active = request.POST.get("status")
        user.save()
        return True
    except Exception as e:
        return False

def del_user(request, username):
    try:
        # import pdb; pdb.set_trace()
        u = User.objects.get(username=username)
        u.delete()
        return True
    except Exception as e:
        return False


def add_user(request):
    try:
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = User.objects.create_user(username, email, password)

        # Add group_name for user
        if request.POST.get("group") == "学生":
            user.group_name = "学生"
        elif request.POST.get("group") == "老师":
            user.group_name = "老师"
        user.save()
        return True
    except Exception as e:
        return False
