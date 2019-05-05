from django.shortcuts import render
from .models import *
from django.views.generic import View
from django.shortcuts import get_object_or_404
# Create your views here.


class UserPosts(View):
    def get(self, request, user_slug):
        posts = Post.objects.all()
        return render(request, "homepage/user_posts.html", context={"posts": posts})


class UserHomepage(View):
    def get(self, request, user_slug):
        posts = Post.objects.all()
        return render(request, "homepage/user_posts.html", context={"posts": posts})


class ViewPost(View):
    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        return render(request, "homepage/view_post.html", context={"post": post})


class RegistrationRequest(View):
    def get(self, request):
        return render(request, "homepage/wannain.html")


def view_post_tags(request):
    tags = PostTag.objects.all()
    return render(request, "homepage/view_tags.html", context={"tags": tags})
