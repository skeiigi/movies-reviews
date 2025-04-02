from django.db import models


class Movies(models.Model):
    title = models.CharField(max_length=50)
    poster = models.ImageField(upload_to='images/', null=True, blank=True)
    about = models.TextField()

    def __str__(self):
        return self.title
