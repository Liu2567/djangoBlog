from django import forms
from .models import Blog, BlogComment


class PubBlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入标题',
                'id': 'blog-title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'id_content',  # wangeditor 同步目标
                'style': 'display: none;'  # 隐藏原始 textarea，用编辑器替代
            })
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': '请输入评论内容...',
                'maxlength': 500,
                'class': 'form-control',
                'style': 'resize: none; width: 100%;',
                'id': 'commentContent'
            })
        }
