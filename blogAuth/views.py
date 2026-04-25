from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from .forms import RegisterForm, LoginForm


# Create your views here.

@require_http_methods(['GET', 'POST'])
def login(request):
    if request.method == 'GET':
        return render(request, 'auth/login.html', {'form': LoginForm()})
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')
            
            user = User.objects.filter(username=username).first()
            if user and check_password(password, user.password):
                # 登录
                auth_login(request, user)
                
                if remember:
                    # 设置session的过期时间
                    request.session.set_expiry(7 * 24 * 60 * 60)
                else:
                    request.session.set_expiry(0)
                
                return redirect('blog:index')
            # else:
            #     form.add_error(None, '用户名或密码错误')
        
        return render(request, 'auth/login.html', {'form': form})


@require_http_methods(['GET', 'POST'])
def register(request):
    if request.method == 'GET':
        return render(request, 'auth/register.html', {'form': RegisterForm()})
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogAuth:login')
        # 重新返回注册页面
        return render(request, 'auth/register.html', {'form': form})


def logout(request):
    """退出登录"""
    auth_logout(request)
    return redirect('blog:index')
