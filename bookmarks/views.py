from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.models import User
from .models import BookmarkFolder
from .forms import CreateBookmarkFolderForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    View
)

# Create your views here.


class UserBookmarksFolders(LoginRequiredMixin, View):
    def get(self, request, user_slug):
        user = User.objects.get(username=user_slug)
        bookmark_folders = BookmarkFolder.objects.filter(author=user)
        context = {"folders": bookmark_folders, "author": user}
        return render(request, "bookmarks/bookmark_folders.html", context=context)


class CreateBookmarkFolder(LoginRequiredMixin, CreateView):
    model = BookmarkFolder
    form_class = CreateBookmarkFolderForm
    template_name = 'bookmarks/create_bookmark_folder.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
