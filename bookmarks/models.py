from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class BookmarkFolder(models.Model):
    title = models.TextField(max_length=100, db_index=True)
    description = models.TextField(max_length=1000, db_index=True)
    slug = models.SlugField(max_length=20)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_hidden = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}"


class Bookmark(models.Model):
    body = models.TextField(max_length=4000, db_index=True, blank=False)
    title = models.TextField(max_length=100, db_index=True, blank=False)
    tags = models.TextField(max_length=500, db_index=True, blank=True)
    slug = models.SlugField(max_length=20)
    folder = models.ForeignKey(BookmarkFolder, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_hidden = models.BooleanField(default=False)
    date_pub = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"
