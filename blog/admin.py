from django.contrib import admin
from .models import Blog, BlogComment

# Register your models here.

# 简单注册
# admin.site.register(Blog)
# admin.site.register(BlogComment)


# 评论内联显示（在博客编辑页直接管理评论）
class BlogCommentInline(admin.TabularInline):
    model = BlogComment
    extra = 1  # 默认显示 1 个空白评论输入框
    fields = ('author', 'content', 'pub_at')
    readonly_fields = ('pub_at',)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    # 1. 列表页显示的字段
    list_display = ('id', 'title', 'author', 'pub_at')

    # 2. 可以点击跳转的字段
    list_display_links = ('title',)

    # 3. 右侧过滤器
    list_filter = ('pub_at', 'author')

    # 4. 顶部搜索框
    search_fields = ('title', 'content')

    # 5. 每页显示的条数
    list_per_page = 20

    # 6. 字段集（编辑页的分组显示）
    fieldsets = (
        ('基础信息', {'fields': ('title', 'author')}),
        ('详细内容', {'fields': ('content',)}),
        ('时间信息', {'fields': ('pub_at',), 'classes': ('collapse',)}),
    )

    # 7. 添加内联评论管理
    inlines = [BlogCommentInline]

    # 设置只读字段（防止手动修改自动生成的时间）
    readonly_fields = ('pub_at',)

# # 注册评论模型（可选，如果只需要在博客页管理评论，可以注释掉下面这行）
# @admin.register(BlogComment)
# class BlogCommentAdmin(admin.ModelAdmin):
#     list_display = ('id', 'content', 'blog', 'author', 'pub_at')
#     list_filter = ('pub_at', 'blog')
#     search_fields = ('content', 'author__username')
#     readonly_fields = ('pub_at',)
