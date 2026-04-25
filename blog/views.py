from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.
# 首页
def index(request):
    return render(request, 'blog/index.html')


# 详情页
def blog_detail(request, blog_id):
    return render(request, 'blog/blog_detail.html')


# 发布页面（需要登录）
@login_required(login_url='blogAuth:login')
# 还有一种方法，@login_required，然后在settings.py中配置LOGIN_URL = '/auth/login'
# 如果页面需要登录后才能访问，也可以在前端中直接隐藏或禁用
def blog_publish(request):
    return render(request, 'blog/blog_publish.html')
