from django import forms
from .models import Blog


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
