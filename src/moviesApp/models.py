from django.db import models
from datetime import datetime


class Movies(models.Model):
    title = models.CharField(max_length=50)
    poster = models.ImageField(upload_to='images/', null=True, blank=True)
    about = models.TextField()

    def __str__(self):
        return self.title


class Reviews(models.Model):
    title = models.CharField(max_length=65)
    movie = models.ForeignKey(Movies, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return self.title
