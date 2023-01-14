from django import forms
from django.contrib.auth.models import User

# 登录表单，继承了 forms.Form 类
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()