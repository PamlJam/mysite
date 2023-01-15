from django import forms
from django.contrib.auth.models import User

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField()
    pwrepeat = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_pwrepeat(self):
        data = self.cleaned_data
        if data.get('password') == data.get('pwrepeat'):
            return data.get('password')
        else:
            raise forms.ValidationError("密码输入不一致，请重试。")