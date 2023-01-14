from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .forms import UserLoginForm

def user_logout(request):
    logout(request)
    return redirect("/")
    #  注销后一定要重定向出去，否则连续注销引发报错

def user_login(request):
# 用户登录视图
    if request.method == 'POST':
        user_login_form = UserLoginForm(data = request.POST)
        # 表单类可以不填入参数实例化，但这种实例无法进行后续的验证
        if user_login_form.is_valid():
        # 如果所有数据都通过验证，则 is_valid() 返回为 True
        # 此时我们将能够在 .cleaned_data 属性中找到所有合法的表单数据所组成的字典
            data = user_login_form.cleaned_data
            # .cleaned_data 清洗出合法数据，数据类型与表单类中字段类型一致
            user = authenticate(username=data['username'], password=data['password'])
            # 检验账号、密码是否正确匹配数据库中的某个用户，如果均匹配则返回这个 user 对象
            if user:
                login(request, user)
                # Django 调用会话组件将用户数据保存在 session 中，实现登录
                # 当用户在 Web 页之间跳转时，存储在 Session 对象中的变量将不会丢失，而是在整个用户会话中一直存在下去
                # Session 最常见的用法就是存储用户的登录数据
                return HttpResponse("登录成功")
            else:
                return HttpResponse("账号或密码输入有误，请重新输入")
        else:
        # 如果只有部分数据通过验证，此时 .cleaned_data 字典只包含合法的字段
            return HttpResponse("账号或密码输入不合法")

    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context = { 'form': user_login_form }
        return render(request, 'userprofile/login.html', context)

    else:
        return HttpResponse("请使用 GET 或 POST 请求数据")