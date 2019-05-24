from django.contrib import admin
from .models import BookmarkFolder, Bookmark
# Register your models here.

admin.site.register(BookmarkFolder)
admin.site.register(Bookmark)
