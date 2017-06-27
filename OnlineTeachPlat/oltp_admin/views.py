# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from oltp_admin.form import RegisterForm

from oltp_admin.models import UserInfo
from django.contrib.auth.models import User, Group
import pdb

from django.views.decorators.csrf import csrf_exempt
# Create your views here.
# superuser root:root_11111 admin:admin_11111


def index(request):
    '''主视图'''
    # 登录则显示index页面
    # 未登录则重定向url = /oltp/login
    # pdb.set_trace()
    User = UserInfo()
    groups = {}
    users = User.Get_all_users()

    # 获取每个用户的组名称
    for user in users:
        pass
        # pdb.set_trace()
        # groups[user.username]=user.groups.all()[0].name

    if request.user.is_authenticated():
        if request.user.username == 'admin':
            # 管理用户
            return render(request, "oltp_admin/admin_index.html", {'users': users})
        else:
            # 普通用户
            return render(request, "oltp_admin/index.html")
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
        form = RegisterForm(request.POST.copy())
        # import pdb; pdb.set_trace()
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
