from django.shortcuts import render
from django.shortcuts import redirect
from django import forms
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .forms import *
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    View
)


# from django.shortcuts import get_object_or_404
# Create your views here.


class UserPosts(View):
    def get(self, request, user_slug):
        posts = Post.objects.all()
        return render(request, "homepage/user_posts.html", context={"posts": posts})


class ViewPost(DetailView):
    model = Post
    template_name = 'homepage/view_post.html'
    # def get(self, request, slug):
    #     post = Post.objects.get(slug=slug)
    #     return render(request, "homepage/view_post.html", context={"post": post})
    def get_context_data(self, object):
        return {"profile": object.author.profile, "post": object}


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'homepage/new_post.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostEdit(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostEditForm
    # fields = ["title", "short_body", "body", "post_tags"]
    template_name = 'homepage/new_post.html'

    # def get(self, request):
    #     form = PostForm()
    #     return render(request, "homepage/new_post.html", context={"form": form})
    #
    # def post(self, request):
    #     bound_form = PostForm(request.POST)
    #     if bound_form.is_valid():
    #         new_post = bound_form.save()
    #         return redirect(new_post)
    #     return render(request, "homepage/new_post.html", context={"form": bound_form})

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    template_name = "homepage/delete_post.html"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


# class RegistrationRequest(View):
#     def get(self, request):
#         return render(request, "homepage/wannain.html")


def view_post_tags(request):
    tags = PostTag.objects.all()
    return render(request, "homepage/view_tags.html", context={"tags": tags})
