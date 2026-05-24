from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # 导入 messages
from .forms import RegisterForm, LoginForm
from blog.models import Blog, BlogComment


# Create your views here.

@require_http_methods(['GET', 'POST'])
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')

            user = authenticate(username=username, password=password)

            if user is not None:
                auth_login(request, user)

                if remember:
                    request.session.set_expiry(7 * 24 * 60 * 60)
                else:
                    request.session.set_expiry(0)

                return redirect('blog:index')
            else:
                form.add_error('username', '用户名或密码错误')
    else:
        form = LoginForm()

    return render(request, 'auth/login.html', {'form': form})


@require_http_methods(['GET', 'POST'])
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "注册成功，请登录！")
            return redirect('blogAuth:login')
    else:
        form = RegisterForm()

    return render(request, 'auth/register.html', {'form': form})


@require_POST
@login_required(login_url='blogAuth:login')
def logout(request):
    """退出登录"""
    auth_logout(request)
    messages.info(request, "您已安全退出")
    return redirect('blog:index')


@require_POST
@login_required(login_url='blogAuth:login')
def delete_account(request):
    """删除账户，注销"""
    user = request.user
    BlogComment.objects.filter(author=user).delete()
    Blog.objects.filter(author=user).delete()
    user.delete()

    return redirect('blog:index')
