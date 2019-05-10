from django.shortcuts import render
from django.shortcuts import redirect

from .models import *

from .forms import *
from django.views.generic import View


# from django.shortcuts import get_object_or_404
# Create your views here.


class UserPosts(View):
    def get(self, request, user_slug):
        posts = Post.objects.all()
        return render(request, "homepage/user_posts.html", context={"posts": posts})


class UserHomepage(View):
    def get(self, request, user_slug):
        posts = Post.objects.all()
        return render(request, "homepage/user_posts.html", context={"posts": posts})


#TODO: edit user complete
class UserHomepageEdit(View):
    def get(self, request):
        user_form = User(request.user)
        profile_form = request.user.profile
        return render(request, "homepage/homepage_edit.html", context={"user_form": user_form,
                                                                       "profile_form": profile_form})


class CurrentUserHomepage(View):
    def get(self, request):
        return render(request, "homepage/homepage.html")


class ViewPost(View):
    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        return render(request, "homepage/view_post.html", context={"post": post})


class PostCreate(View):
    def get(self, request):
        form = PostForm()
        return render(request, "homepage/new_post.html", context={"form": form})

    def post(self, request):
        bound_form = PostForm(request.POST)
        if bound_form.is_valid():
            new_post = bound_form.save()
            return redirect(new_post)
        return render(request, "homepage/new_post.html", context={"form": bound_form})


# class RegistrationRequest(View):
#     def get(self, request):
#         return render(request, "homepage/wannain.html")


def view_post_tags(request):
    tags = PostTag.objects.all()
    return render(request, "homepage/view_tags.html", context={"tags": tags})
