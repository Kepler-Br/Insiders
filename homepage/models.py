from django.db import models
from django.shortcuts import reverse

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, unique=True)
    body = models.TextField(max_length=6000, db_index=True)
    short_body = models.TextField(max_length=1000, blank=True)
    post_tags = models.TextField(max_length=1000, blank=True, db_index=True)
    date_pub = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse("post_detail_url", kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class InviteLinkList(models.Model):
    slug = models.SlugField(max_length=15, unique=True)
