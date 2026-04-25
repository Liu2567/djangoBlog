from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    pub_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class BlogComment(models.Model):
    content = models.TextField()
    pub_at = models.DateTimeField(auto_now_add=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
