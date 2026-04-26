from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from blog.forms import PubBlogForm
from blog.models import Blog, BlogComment
from django.db.models import Q


# Create your views here.
# 首页
def index(request):
    blogs = Blog.objects.all()
    return render(request, 'blog/index.html', {
        'blogs': blogs,
        'keyword': '',
        'search_mode': False
    })

# 详情页
def blog_detail(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    comments = BlogComment.objects.filter(blog=blog)
    return render(request, 'blog/blog_detail.html', {'blog': blog, 'comments': comments})


# 发布页面（需要登录）
@require_http_methods(['GET', 'POST'])
@login_required(login_url='blogAuth:login')
# 还有一种方法，@login_required，然后在settings.py中配置LOGIN_URL = '/auth/login'
# 如果页面需要登录后才能访问，也可以在前端中直接隐藏或禁用
def blog_publish(request):
    if request.method == 'GET':
        form = PubBlogForm()
        return render(request, 'blog/blog_publish.html', {'form': form})
    else:
        form = PubBlogForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')

            # 1. 获取 create 返回的新对象
            blog = Blog.objects.create(title=title, content=content, author=request.user)

            # 2. 使用对象的 id 属性进行跳转
            return redirect('blog:blog_detail', blog_id=blog.id)
        else:
            return render(request, 'blog/blog_publish.html', {'form': form})


# 评论
@require_POST
@login_required(login_url='blogAuth:login')
def blog_comment(request):
    blog_id = request.POST.get('blog_id')
    content = request.POST.get('content')
    BlogComment.objects.create(content=content, blog_id=blog_id, author=request.user)

    # 发布后重新加载详情页
    return redirect('blog:blog_detail', blog_id=blog_id)


# 搜索
@require_GET
def search(request):
    # /search?keyword=xxxx
    # 获取关键词并去除首尾空格
    keyword = request.GET.get('keyword', '').strip()
    
    # 如果关键词为空（包括只输入空格的情况），直接返回全部博客
    if not keyword:
        blogs = Blog.objects.all()
        return render(request, 'blog/index.html', {
            'blogs': blogs,
            'keyword': '',
            'search_mode': False
        })
    
    # 如果有有效关键词 搜索
    blogs = Blog.objects.filter(Q(title__icontains=keyword) | Q(content__icontains=keyword))
    
    return render(request, 'blog/index.html', {
        'blogs': blogs,
        'keyword': keyword,
        'search_mode': True
    })