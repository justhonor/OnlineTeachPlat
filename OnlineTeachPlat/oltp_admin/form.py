# coding=utf-8
from django import forms
from django.contrib.auth.models import User,Group

import pdb
# Register your models here.
ALLOW_CHAR = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


class RegisterForm(forms.Form):
    """docstring for RegisterForm"""
    # max_length 限制表单输入的字符数
    username = forms.CharField(label="昵称:  ", max_length=40,
                               widget=forms.TextInput(attrs={'size': 40, 'class': "form-control"}))
    email = forms.EmailField(label=u"邮件:  ", max_length=40,
                             widget=forms.EmailInput(attrs={'size': 40, 'class': "form-control"}))
    password = forms.CharField(label=u"密码:", max_length=20,
                               widget=forms.PasswordInput(attrs={'size': 20, 'class': "form-control"}))
    re_password = forms.CharField(label=u"确认密码:", max_length=20,
                                  widget=forms.PasswordInput(attrs={'size': 20, 'class': "form-control"}))
    # student = forms.RadioSelect()
    # teacher = forms.RadioSelect()

    student = forms.RadioSelect()
    teacher = forms.CharField()

    def clean_username(self):
        ''' 验证昵称'''
        if len(self.cleaned_data["username"]) < 2:
            raise forms.ValidationError("昵称长度不能小于4")
        else:
            for a in self.cleaned_data["username"]:
                if a not in ALLOW_CHAR:
                    raise forms.ValidationError("昵称仅能用字母或数字")

        users = User.objects.filter(
            username__iexact=self.cleaned_data["username"])
        if not users:
            return self.cleaned_data["username"]
        else:
            raise forms.ValidationError(u"该昵称已经被使用请使用其他的昵称")

    def clean_email(self):
        '''验证重复email'''
        emails = User.objects.filter(email__iexact=self.cleaned_data["email"])
        if not emails:
            return self.cleaned_data["email"]
        raise forms.ValidationError(u"该邮箱已经被使用请使用其他的邮箱")

    def clean_password(self):
        if len(self.cleaned_data["password"]) < 3:
            raise forms.ValidationError(u"密码长度不能小于6")
        else:
            for a in self.cleaned_data["password"]:
                if a not in ALLOW_CHAR:
                    raise forms.ValidationError(u"密码仅能用字母或数字")
        return self.cleaned_data["password"]

    def clean(self):
        """验证其他非法"""

        cleaned_data = super(RegisterForm, self).clean()

        # 防止由于有未提交的表单引起的form.is_valid()==flase
        if cleaned_data.get("student") == "on":
            cleaned_data.update({"teacher":"off"})
        elif cleaned_data.get("teacher") == "on":
            cleaned_data.update({"student":"off"})
        # pdb.set_trace()
        
        # 验证是否选择分组
        if cleaned_data.get("student") != "on" and cleaned_data.get("teacher") != "on":
            raise forms.ValidationError(u"您必须选取一个分组!!!")

        if cleaned_data.get("password") == cleaned_data.get("username"):
            raise forms.ValidationError(u"用户名和密码不能一样")
        if cleaned_data.get("password") != cleaned_data.get("re_password"):
            raise forms.ValidationError(u"两次输入密码不一致!!!")

        return cleaned_data

    '''
    group = Group.objects.get(name='groupname')     # select a group
    group = Group(name="Editor")                    # create a group named Editor
    group.save()                                    # save this new group for this example
    user = User.objects.get(pk=1)                   # assuming, there is one initial user 
    user.groups.add(group)                          # user is now in the "Editor" group

    '''

    def save(self):

        username = self.cleaned_data["username"]
        email = self.cleaned_data["email"]
        password = self.cleaned_data["password"]
        user = User.objects.create_user(username, email, password)
        
        # Add group_name for user 
        if self.cleaned_data["student"] == "on":
            user.group_name = "学生"
        elif self.cleaned_data["teacher"] == "on":
            user.group_name = "老师"
        user.save()
        
        return user
