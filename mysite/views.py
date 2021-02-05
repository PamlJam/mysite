from django.contrib import auth
from django.shortcuts import render, render_to_response,get_object_or_404
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import redirect
from .forms import LoginForm
from .forms import RegForm
from django.contrib.auth.models import User

def home(request):
    context={}
    return render_to_response('home.html',context)

def loginto(request): 
    if request.method == "POST":
    # 提交数据
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
        # 数据有效,排除异常输入
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = auth.authenticate(request,username= username, password= password)
            if user is not None:
            # 登录成功
                login(request, user)
                return redirect(request.POST.get('from','/'))
                # 获取网址参数form，比如http://127.0.0.1:8000/login/?from=/blog/6
                # 本欲重定向上一页，但是失败了...只能去首页 
            else:
            # 显示错误信息
                login_form.add_error(None,"用户名或者密码错误")
    else:
        login_form = LoginForm()
    context = {}
    context['login_form'] = login_form
    return render(request,'login.html',context)


def register(request):
    if request.method == "POST":
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            u = reg_form.cleaned_data['username']
            e = reg_form.cleaned_data['email']
            p = reg_form.cleaned_data['password']
            newuser = User.objects.create_user(u,e,p)
            # 创建新用户
            newuser.save()
            return HttpResponse('已注册')
    else:
        reg_form = RegForm()
    context = {}
    context['reg_form'] = reg_form
    return render(request,'register.html',context)

