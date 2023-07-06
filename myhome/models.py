from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=20)
    image = models.CharField(max_length=100,null=True,blank=True)
    author = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=None)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey('Post',on_delete=models.CASCADE)


