from django.db import models

# Create your models here.


class InviteLinkList(models.Model):
    slug = models.SlugField(max_length=15, unique=True)


class InviteRequests(models.Model):
    username = models.TextField(max_length=256, unique=True, blank=False)
    firstname = models.TextField(max_length=50, blank=False)
    secondname = models.TextField(max_length=50, blank=True)
    contacts = models.TextField(max_length=500, blank=False)
    about = models.TextField(max_length=2000, blank=False)
