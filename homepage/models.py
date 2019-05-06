from django.db import models
from django.shortcuts import reverse

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, unique=True)
    body = models.TextField(blank=True, db_index=True)
    date_pub = models.DateTimeField(auto_now_add=True)
    # post_tags = models.ManyToManyField('PostTag', blank=True, related_name="posts")

    def get_absolute_url(self):
        return reverse("post_detail_url", kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class PostTag(models.Model):
    title = models.CharField(max_length=50)

    # def get_absolute_url(self):
    #     return reverse("posts_with_tag", kwargs={'slug': self.tag_name})

    def __str__(self):
        return self.title
