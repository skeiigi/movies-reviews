from django.conf import settings
from django.db import models
from datetime import datetime


class Country(models.Model):
    name = models.TextField(unique=True)

    def __str__(self):
        return self.name


class Movies(models.Model):
    title = models.CharField(max_length=50)
    poster = models.ImageField(upload_to='images/', null=True, blank=True)
    about = models.TextField()
    duration_minutes = models.PositiveIntegerField(verbose_name="Продолжительность", null=True)
    country_release = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    changed_at = models.DateTimeField(auto_now=True, null=True)
    removed = models.BooleanField(default=False, null=False)

    def __str__(self):
        return self.title

    def get_duration(self):
        hours = self.duration_minutes // 60
        minutes = self.duration_minutes % 60

        return f"{hours}ч {minutes}мин"


class Reviews(models.Model):
    title = models.CharField(max_length=65)
    movie = models.ForeignKey(
        Movies,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    changed_at = models.DateTimeField(auto_now=True, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=False,
        null=True
    )
    removed = models.BooleanField(default=False, null=False)

    def __str__(self):
        return self.title


class Comment(models.Model):
    review = models.ForeignKey(Reviews, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    removed = models.BooleanField(default=False, null=False)

    def __str__(self):
        return f'Комментарий от {self.user.username}'


class Notification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    removed = models.BooleanField(default=False, null=False)

    def __str__(self):
        return f'Уведомление для {self.recipient.username}'
