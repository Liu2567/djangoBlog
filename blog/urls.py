from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('blog/detail/<int:blog_id>', views.blog_detail, name='blog_detail'),
    path('blog/publish', views.blog_publish, name='blog_publish'),
    path('blog/comment', views.blog_comment, name='blog_comment'),
    path('blog/search', views.search, name='search'),
    path('blog/my_publish', views.my_publish, name='my_publish'),
    path('blog/<int:blog_id>/edit', views.blog_edit, name='blog_edit'),
    path('blog/<int:blog_id>/delete', views.blog_delete, name='blog_delete'),
    path('profile', views.profile, name='profile')
]
