from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class InviteLinkList(models.Model):
    slug = models.SlugField(max_length=15, unique=True)


class InviteRequests(models.Model):
    username = models.TextField(max_length=256, unique=True, blank=False)
    firstname = models.TextField(max_length=50, blank=False)
    secondname = models.TextField(max_length=50, blank=True)
    contacts = models.TextField(max_length=500, blank=False)
    about = models.TextField(max_length=2000, blank=False)


class Profile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('U', 'Undefined'),
        ('H', 'Helisexual'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pictures/default_avatar.png', upload_to="profile_pictures")
    # short_about = models.CharField(max_length=100, blank=True)
    about = models.CharField(max_length=1000, blank=True)
    status = models.CharField(max_length=256, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='U')

    def __str__(self):
        return f"{self.user.username}'s profile"

