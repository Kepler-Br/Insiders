from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View
from django.contrib.auth.models import User
from .models import BookmarkFolder, Bookmark
from .forms import BookmarkFolderForm, BookmarkForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    View
)
from django import forms

# Create your views here.


class UserBookmarksFolders(LoginRequiredMixin, View):
    def get(self, request, slug):
        user = User.objects.get(username=slug)
        bookmark_folders = BookmarkFolder.objects.filter(author=user)
        if not user == request.user:
            bookmark_folders = bookmark_folders.filter(is_hidden=False)
        context = {"folders": bookmark_folders, "author": user}
        return render(request, "bookmarks/bookmark_folders.html", context=context)


class ViewBookmarkFolder(LoginRequiredMixin, View):
    def get(self, request, slug):
        folder = BookmarkFolder.objects.get(slug=slug)
        bookmarks = Bookmark.objects.filter(folder=folder)
        context = {"bookmarks": bookmarks, "folder": folder}
        return render(request, "bookmarks/view_bookmark_folder.html", context=context)


class ViewBookmark(LoginRequiredMixin, View):
    def get(self, request, slug):
        bookmark = Bookmark.objects.get(slug=slug)
        context = {"bookmark": bookmark}
        return render(request, "bookmarks/view_bookmark.html", context=context)


class CreateBookmarkFolder(LoginRequiredMixin, CreateView):
    model = BookmarkFolder
    form_class = BookmarkFolderForm
    template_name = 'bookmarks/create_bookmark_folder.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CreateBookmark(LoginRequiredMixin, CreateView):
    model = Bookmark
    form_class = BookmarkForm
    template_name = 'bookmarks/create_bookmark.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class
        folders = BookmarkFolder.objects.filter(author=request.user)
        form.base_fields["folder"] = forms.ModelChoiceField(queryset=folders)
        context = {"form": form}
        return render(request, "bookmarks/create_bookmark.html", context=context)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class DeleteBookmarkFolder(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BookmarkFolder
    template_name = "bookmarks/delete_bookmark_folder.html"

    def get_success_url(self):
        # Assuming there is a ForeignKey from Comment to Post in your model
        folder = self.object
        return reverse_lazy('user_bookmark_folders', kwargs={'slug': folder.author.username})

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class EditBookmark(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Bookmark
    form_class = BookmarkForm
    template_name = 'bookmarks/bookmarks_edit_generic_page.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=Bookmark.objects.get(slug=kwargs["slug"]))
        folders = BookmarkFolder.objects.filter(author=request.user)
        form.base_fields["folder"] = forms.ModelChoiceField(queryset=folders)
        context = {"form": form}
        return render(request, "bookmarks/bookmarks_edit_generic_page.html", context=context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES, instance=Bookmark.objects.get(slug=kwargs["slug"]))
        if form.is_valid():
            form.save()
            return redirect("user_home", user_slug=request.user.username)
        else:
            context = {"form": form}
            return render(request, self.template_name, context=context)

    def form_valid(self, form):
        # form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        bookmark = self.get_object()
        if self.request.user == bookmark.author:
            return True
        return False


class EditBookmarkFolder(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BookmarkFolder
    form_class = BookmarkFolderForm
    template_name = 'bookmarks/bookmarks_edit_generic_page.html'

    def form_valid(self, form):
        # form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        bookmark_folder = self.get_object()
        if self.request.user == bookmark_folder.author:
            return True
        return False


class DeleteBookmark(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Bookmark
    template_name = "bookmarks/delete_bookmark.html"

    def get_success_url(self):
        # Assuming there is a ForeignKey from Comment to Post in your model
        folder = self.object.folder
        return reverse_lazy('bookmark_folder', kwargs={'slug': folder.slug})

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
