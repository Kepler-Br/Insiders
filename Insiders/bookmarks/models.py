from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse

# Create your models here.


class BookmarkFolder(models.Model):
    title = models.TextField(max_length=100, db_index=True)
    description = models.TextField(max_length=1000, db_index=True)
    slug = models.SlugField(max_length=20)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_hidden = models.BooleanField(default=False)
    image = models.ImageField(default='bookmark_folder_avatars/default_avatar.png', upload_to="bookmark_folder_avatars")

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse('bookmark_folder', kwargs={'slug': self.slug})


class Bookmark(models.Model):
    body = models.TextField(max_length=4000, db_index=True, blank=False)
    image = models.ImageField(default='bookmark_avatars/default_avatar.png', upload_to="bookmark_avatars")
    title = models.TextField(max_length=100, db_index=True, blank=False)
    tags = models.TextField(max_length=500, db_index=True, blank=True)
    slug = models.SlugField(max_length=20)
    folder = models.ForeignKey(BookmarkFolder, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_hidden = models.BooleanField(default=False)
    date_pub = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse('bookmark', kwargs={'slug': self.slug})


