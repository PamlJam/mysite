from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .forms import UserLoginForm, UserRegisterForm

def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(data = request.POST)
        if form.is_valid():
            new_user = form.save(commit = False)
            new_user.set_password(form.cleaned_data['password'])
            # 一个经典错误：new_user.password = form.cleaned_data['password'] 
            # 此时所设置密码是明文，无法进行认证 auth.authenticate()
            new_user.save()
            login(request, new_user)
            return redirect("/")
        else:
            return HttpResponse("注册表单输入有误。请重新输入")

    elif request.method == 'GET':
    # 保留用户已经输入的内容
        user_register_form = UserRegisterForm()
        context = { 'form': user_register_form }
        return render(request, 'userprofile/register.html', context)
    else:
        return HttpResponse("请使用 GET 或 POST 请求数据")

def user_logout(request):
    logout(request)
    return redirect("/")

def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(data = request.POST)
        if user_login_form.is_valid():
            data = user_login_form.cleaned_data
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                login(request, user)
                return HttpResponse("登录成功")
            else:
                return HttpResponse("账号或密码输入有误，请重新输入")
        else:
            return HttpResponse("账号或密码输入不合法")

    elif request.method == 'GET':
    # 保留用户已经输入的内容
        user_login_form = UserLoginForm()
        context = { 'form': user_login_form }
        return render(request, 'userprofile/login.html', context)
    else:
        return HttpResponse("请使用 GET 或 POST 请求数据")