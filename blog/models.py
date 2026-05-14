from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    pub_at = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')

    class Meta:
        verbose_name = '博客'
        verbose_name_plural = verbose_name
        ordering = ['-pub_at']

    def __str__(self):
        return self.title


class BlogComment(models.Model):
    content = models.TextField(verbose_name='内容')
    pub_at = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name='所属博客')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')

    class Meta:
        verbose_name = '博客评论'
        verbose_name_plural = verbose_name
        ordering = ['-pub_at']
