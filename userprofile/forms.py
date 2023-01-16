from django import forms
from django.contrib.auth.models import User
from django.forms import ValidationError

def check_password(passwd):
# 用于验证密码的有效性
    hint = ''

    if len(passwd) < 6:
        hint = '密码长度至少为 6'
         
    if len(passwd) > 20:
        hint = '密码长度至多为 20'
         
    if not any(char.isdigit() for char in passwd):
        hint = '密码需要包含数字'
         
    if not any(char.isupper() for char in passwd):
        hint =  '密码需要包含大写字母'
         
    if not any(char.islower() for char in passwd):
        hint = '密码需要包含小写字母'

    if not passwd.isalnum():
        hint = '密码只能由数字与字母组成'

    return hint

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField()
    repeat = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_username(self):
    # 覆写局部钩子
        un = self.cleaned_data.get('username')
        user = User.objects.filter(username = un).first()
        if user:
            raise ValidationError('用户已经存在')
        else:
            return un

    def clean_password(self):
    # 覆写局部钩子
        pw = self.cleaned_data.get('password')
        hint = check_password(pw)
        if hint:
            raise forms.ValidationError(hint)
        else:
            return pw

    # def clean_repeat(self):
    # 也可以在这验证，但是比较麻烦

    def clean(self):
    # 如果验证数据的时候，需要针对多个字段进行验证，那么最好覆写全局钩子
        pw = self.cleaned_data.get('password')
        re = self.cleaned_data.get('repeat')
        if pw == re:
            return pw
        else:
            return self.add_error('repeat','两次输入的密码不一致')
            # 这样比直接在 clean_repeat 中 raise ValidationError 要好得多