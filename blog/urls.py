from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('blog/detail/<int:blog_id>', views.blog_detail, name='blog_detail'),
    path('blog/publish', views.blog_publish, name='blog_publish'),
    path('blog/comment', views.blog_comment, name='blog_comment'),
]
