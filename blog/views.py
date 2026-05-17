from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from blog.forms import PubBlogForm, CommentForm
from blog.models import Blog, BlogComment
from django.db.models import Q
from django.core.paginator import Paginator


# 首页
def index(request):
    blogs = Blog.objects.select_related('author').all()
    paginator = Paginator(blogs, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/index.html', {
        'page_obj': page_obj,
        'search_mode': False
    })


# 详情页
def blog_detail(request, slug):
    try:
        blog = Blog.objects.select_related('author').get(slug=slug)
    except Blog.DoesNotExist:
        return redirect('blog:index')

    comments = BlogComment.objects.select_related('author').filter(blog=blog)

    form = CommentForm()

    return render(request, 'blog/blog_detail.html',
                  {'blog': blog, 'comments': comments, 'form': form})


# 发布页面（需要登录）
@require_http_methods(['GET', 'POST'])
@login_required(login_url='blogAuth:login')
def blog_publish(request):
    if request.method == 'POST':
        form = PubBlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect('blog:blog_detail', slug=blog.slug)
    else:
        form = PubBlogForm()

    return render(request, 'blog/blog_publish.html', {'form': form})


# 评论
@require_POST
@login_required(login_url='blogAuth:login')
def blog_comment(request):
    blog_id = request.POST.get('blog_id')

    try:
        blog = Blog.objects.get(id=blog_id)
    except Blog.DoesNotExist:
        return redirect('blog:index')

    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.blog = blog
        comment.save()
        return redirect('blog:blog_detail', slug=blog.slug)
    else:
        return redirect('blog:blog_detail', slug=blog.slug)


# 删除评论
@require_POST
@login_required(login_url='blogAuth:login')
def blog_comment_delete(request, comment_id):
    try:
        comment = BlogComment.objects.select_related('author', 'blog').get(id=comment_id)
    except BlogComment.DoesNotExist:
        return redirect('blog:index')

    if comment.author != request.user:
        return redirect('blog:blog_detail', slug=comment.blog.slug)

    comment.delete()

    return redirect('blog:blog_detail', slug=comment.blog.slug)


# 搜索
@require_GET
def search(request):
    keyword = request.GET.get('keyword', '').strip()
    scope = request.GET.get('scope', 'all')

    if scope == 'my':
        if not request.user.is_authenticated:
            return redirect('blogAuth:login')
        blogs = Blog.objects.select_related('author').filter(author=request.user)
        template_name = 'blog/my_publish.html'
    else:
        blogs = Blog.objects.select_related('author').all()
        template_name = 'blog/index.html'

    if keyword:
        blogs = blogs.filter(Q(title__icontains=keyword) | Q(content__icontains=keyword))
        search_mode = True
    else:
        search_mode = False

    paginator = Paginator(blogs, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, template_name, {
        'page_obj': page_obj,
        'keyword': keyword,
        'search_mode': search_mode
    })


# 我的发布（需要登录）
@login_required(login_url='blogAuth:login')
def my_publish(request):
    blogs = Blog.objects.select_related('author').filter(author=request.user)
    paginator = Paginator(blogs, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/my_publish.html', {'page_obj': page_obj})


# 编辑博客
@require_http_methods(['GET', 'POST'])
@login_required(login_url='blogAuth:login')
def blog_edit(request, slug):
    try:
        blog = Blog.objects.select_related('author').get(slug=slug)
    except Blog.DoesNotExist:
        return redirect('blog:index')

    if blog.author != request.user:
        return redirect('blog:blog_detail', slug=blog.slug)

    if request.method == 'POST':
        form = PubBlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('blog:blog_detail', slug=blog.slug)
    else:
        form = PubBlogForm(instance=blog)

    return render(request, 'blog/blog_publish.html', {'form': form, 'blog': blog})


# 删除博客
@require_POST
@login_required(login_url='blogAuth:login')
def blog_delete(request, slug):
    try:
        blog = Blog.objects.select_related('author').get(slug=slug)
    except Blog.DoesNotExist:
        return redirect('blog:index')

    if blog.author != request.user:
        return redirect('blog:blog_detail', slug=blog.slug)

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
