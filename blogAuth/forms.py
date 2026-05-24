from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        min_length=3,  # Django 后端验证
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': '请输入用户名',
            'required': True,   # 1. HTML5 必填
            'minlength': 3,     # 2. HTML5 最小长度
            'maxlength': 10     # 3. HTML5 最大长度
        }),
        error_messages={
            'required': '用户名不能为空',
            'min_length': '用户名长度不能小于3个字符',
            'max_length': '用户名长度不能大于10个字符'
        }
    )
    password = forms.CharField(
        label='密码',
        min_length=6,
        max_length=20,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': '请输入密码',
            'required': True,
            'minlength': 6,
            'maxlength': 20
        }),
        error_messages={
            'required': '密码不能为空',
            'min_length': '密码长度不能小于6个字符',
            'max_length': '密码长度不能大于20个字符'
        }
    )
    confirm_password = forms.CharField(
        label='确认密码',
        min_length=6,
        max_length=20,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': '请输入确认密码',
            'required': True,
            'minlength': 6,
            'maxlength': 20
        }),
        error_messages={
            'required': '确认密码不能为空',
            'min_length': '密码长度不能小于6个字符',
            'max_length': '密码长度不能大于20个字符'
        }
    )

    def clean_username(self):
        """验证用户名是否已存在"""
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username=username).exists():
            raise forms.ValidationError('该用户名已被注册')
        return username

    def clean(self):
        """验证密码和确认密码是否一致"""
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', '两次输入的密码不一致')

        return cleaned_data

    def save(self):
        """保存用户"""
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = User.objects.create_user(username=username, password=password)
        return user


class LoginForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        min_length=3,
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': '请输入用户名',
            'required': True,
            'minlength': 3,
            'maxlength': 10
        }),
        error_messages={
            'required': '用户名不能为空',
            'min_length': '用户名长度不能小于3个字符',
            'max_length': '用户名长度不能大于10个字符'
        }
    )
    password = forms.CharField(
        label='密码',
        min_length=6,
        max_length=20,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': '请输入密码',
            'required': True,
            'minlength': 6,
            'maxlength': 20
        }),
        error_messages={
            'required': '密码不能为空',
            'min_length': '密码长度不能小于6个字符',
            'max_length': '密码长度不能大于20个字符'
        }
    )
    remember = forms.BooleanField(
        label='记住我',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
