from django.db import models
from django.contrib.auth.models import User

class Comment(models.Model):
    by = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class Quote(models.Model):
    quote = models.TextField()
    by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) 
    likes = models.ManyToManyField(Like)
    comments = models.ManyToManyField(Comment)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
