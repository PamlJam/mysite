from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    # 密码设置暗文
class RegForm(forms.Form):
    username = forms.CharField(label= '用户名',
                                max_length= 10,
                                min_length= 5, )

    email =forms.CharField(label='邮箱')

    password = forms.CharField(label='密码',
                                min_length= 5,
                                max_length= 20, 
                                widget=forms.PasswordInput)
    
    password_again = forms.CharField(label='再次输入密码',
                                min_length= 5, 
                                max_length= 20,
                                widget=forms.PasswordInput)
    def clean_username(self):
        u = self.cleaned_data['username']
        if User.objects.filter(username= u).exists():
            raise forms.ValidationError('用户名已存在')
        return u

    def clean_email(self):
        e = self.cleaned_data['email']
        if User.objects.filter(username= e).exists():
            raise forms.ValidationError('邮箱已注册')
        return e
    def clean_password_again(self):
        p = self.cleaned_data['password']
        a = self.cleaned_data['password_again']
        if p != a:
            raise forms.ValidationError('密码输入不一致')
        return p
