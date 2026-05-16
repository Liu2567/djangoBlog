from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils.text import slugify
from pypinyin import pinyin, Style


# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='标题')
    slug = models.SlugField(max_length=100, unique=True, blank=True, verbose_name='URL别名')
    content = models.TextField(verbose_name='内容')
    pub_at = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')

    def _generate_unique_slug(self):
        py_list = pinyin(self.title, style=Style.NORMAL)
        title_py = '-'.join([item[0] for item in py_list])
        
        base_slug = slugify(title_py)[:30].rstrip('-')

        if not base_slug:
            base_slug = str(uuid.uuid4())[:6]

        unique_slug = f"{base_slug}-{uuid.uuid4().hex[:6]}"

        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug or Blog.objects.filter(pk=self.pk).exclude(title=self.title).exists():
            self.slug = self._generate_unique_slug()
        super().save(*args, **kwargs)

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
