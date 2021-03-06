from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, unique=True)
    body = models.TextField(max_length=6000, db_index=True)
    processed_body = models.TextField(max_length=6000, blank=True)
    short_body = models.TextField(max_length=1000, blank=True)
    processed_short_body = models.TextField(max_length=1000, blank=True)
    post_tags = models.TextField(max_length=1000, blank=True, db_index=True)
    date_pub = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title