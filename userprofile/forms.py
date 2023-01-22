from django import forms
from django.contrib.auth.models import User
from django.forms import ValidationError

def check_username(usernm):
# 用于验证用户名的有效性
    hint = ''
    if not usernm.encode().isalnum():
        hint = '用户名只能由数字与字母组成'
    if len(usernm) < 3:
        hint = '用户名长度至少为 3'
    if len(usernm) > 20:
        hint = '用户名长度至多为 20'

    return hint

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

    if not passwd.encode().isalnum():
    # 密码不能为中文 https://blog.csdn.net/weixin_43667990/article/details/88629829
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

    def clean_email(self):
    # 我们在保持原有功能的基础上，增加判断重复邮箱功能
    # 至于为什么能够保持其原有功能，详见 https://stackoverflow.com/a/1872108/20897534
        user = User.objects.filter(email = em).first()
        if user:
            raise forms.ValidationError('此邮箱已被人使用')
        return em

    def clean_username(self):
    # 覆写局部钩子
        un = self.cleaned_data.get('username')
        user = User.objects.filter(username = un).first()
        if user:
            raise ValidationError('用户名已经存在')
        hint = check_username(un)
        # 检查用户名格式
        if hint:
            raise forms.ValidationError(hint)
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
            return self.cleaned_data
            # 全局钩子必须返回所有数据
        else:
            return self.add_error('repeat','两次输入的密码不一致')
            # 这样比直接在 clean_repeat 中 raise ValidationError 要好得多