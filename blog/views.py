from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from blog.forms import PubBlogForm
from blog.models import Blog, BlogComment
from django.db.models import Q
from django.core.paginator import Paginator


# Create your views here.
# 首页
def index(request):
    # 使用 select_related 优化，避免 N+1 查询问题
    blogs = Blog.objects.select_related('author').all()
    
    # 创建分页器，每页显示 6 篇博客
    paginator = Paginator(blogs, 6)
    
    # 获取当前页码（从 URL 参数中获取）
    page_number = request.GET.get('page')
    
    # 获取当前页的对象
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'blog/index.html', {
        'page_obj': page_obj,
        'blogs': page_obj,  # 保持兼容性，模板中可以用 page_obj 或 blogs
        'keyword': '',
        'search_mode': False
    })


# 详情页
def blog_detail(request, blog_id):
    try:
        # 预加载博客作者
        blog = Blog.objects.select_related('author').get(id=blog_id)
    except Blog.DoesNotExist:
        return redirect('blog:index')
    
    # 预加载评论及其作者
    comments = BlogComment.objects.select_related('author').filter(blog=blog)
    
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
    content = request.POST.get('content', '').strip()
    
    # 验证内容不为空
    if not content:
        return redirect('blog:blog_detail', blog_id=blog_id)
    
    try:
        blog = Blog.objects.get(id=blog_id)
    except Blog.DoesNotExist:
        return redirect('blog:index')

    BlogComment.objects.create(content=content, blog=blog, author=request.user)

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
        blogs = Blog.objects.select_related('author').all()
        
        # 添加分页
        paginator = Paginator(blogs, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        return render(request, 'blog/index.html', {
            'page_obj': page_obj,
            'blogs': page_obj,
            'keyword': '',
            'search_mode': False
        })

    # 如果有有效关键词 搜索，同时预加载作者
    blogs = Blog.objects.select_related('author').filter(
        Q(title__icontains=keyword) | Q(content__icontains=keyword)
    )
    
    # 添加分页
    paginator = Paginator(blogs, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/index.html', {
        'page_obj': page_obj,
        'blogs': page_obj,
        'keyword': keyword,
        'search_mode': True
    })


# 我的发布
@login_required(login_url='blogAuth:login')
def my_publish(request):
    # 使用 select_related 优化查询
    blogs = Blog.objects.select_related('author').filter(author=request.user)
    
    # 添加分页
    paginator = Paginator(blogs, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'blog/my_publish.html', {
        'page_obj': page_obj,
        'blogs': page_obj
    })


# 编辑博客
@require_http_methods(['GET', 'POST'])
@login_required(login_url='blogAuth:login')
def blog_edit(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    # 验证是否是作者本人
    if blog.author != request.user:
        return redirect('blog:blog_detail', blog_id=blog_id)

    if request.method == 'GET':
        form = PubBlogForm(instance=blog)
        return render(request, 'blog/blog_publish.html', {'form': form, 'blog': blog})
    else:
        form = PubBlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()  # 保存
            return redirect('blog:blog_detail', blog_id=blog_id)
        else:
            return render(request, 'blog/blog_publish.html', {'form': form, 'blog': blog})


# 删除博客
@require_POST
@login_required(login_url='blogAuth:login')
def blog_delete(request, blog_id):
    try:
        blog = Blog.objects.get(id=blog_id)
    except Blog.DoesNotExist:  # 没有找到该博客
        return redirect('blog:index')

    if blog.author != request.user:
        return redirect('blog:blog_detail', blog_id=blog_id)

    blog.delete()
    return redirect('blog:my_publish')


@login_required(login_url='blogAuth:login')
def profile(request):
    user = request.user
    blog_count = Blog.objects.filter(author=user).count()

    context = {
        'user': user,
        'blog_count': blog_count,
    }

    return render(request, 'blog/profile.html', context=context)
