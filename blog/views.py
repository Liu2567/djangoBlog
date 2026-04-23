from django.shortcuts import render


# Create your views here.
# 首页
def index(request):
    return render(request, 'blog/index.html')


# 详情页
def blog_detail(request, blog_id):
    return render(request, 'blog/blog_detail.html')


# 发布页面
def blog_publish(request):
    return render(request, 'blog/blog_publish.html')
