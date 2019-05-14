from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.models import User
from .models import BookmarkFolder
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.


class UserBookmarksFolders(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, user_slug):
        user = User.objects.get(username=user_slug)
        bookmark_folders = BookmarkFolder.objects.filter(author=user)
        context = {"folders": bookmark_folders}
        return render(request, "bookmarks/bookmark_folders.html", context=context)
