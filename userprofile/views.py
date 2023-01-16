from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .forms import UserLoginForm, UserRegisterForm
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET","POST"])  # 只允许这两种方法
def user_register(request):
    if request.user.is_authenticated:
    # 只允许未登录的游客访问此视图
        return redirect("/")

    if request.method == 'GET':
        return render(request, 'userprofile/register.html')

    if request.method == 'POST':
        form = UserRegisterForm(data = request.POST)
        if form.is_valid():
            new_user = form.save(commit = False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            login(request, new_user)
            return redirect("/")
        else:
            errorDict = form.errors
    return render(request, 'userprofile/register.html', {"errorDict" : errorDict})

@require_http_methods(["GET","POST"])  # 只允许这两种方法
def user_login(request):
    if request.user.is_authenticated:
    # 只允许未登录的游客访问此视图
        return redirect("/")

    if request.method == 'GET':
        return render(request, 'userprofile/login.html')

    if request.method == 'POST':
        form = UserLoginForm(data = request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                login(request, user)
                return redirect("/")
            else:
                form.add_error('password', "用户名或密码错误")
                # 为 form.errors 字典增加错误信息

        errorDict = form.errors        
        return render(request, 'userprofile/login.html', {"errorDict" : errorDict})

def user_logout(request):
    logout(request)
    return redirect("/")