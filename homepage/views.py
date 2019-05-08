from django.shortcuts import render
from django.shortcuts import redirect
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from .forms import *
from django.views.generic import View
from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout
# from django.shortcuts import get_object_or_404
# Create your views here.


class LogoutPage(View):
    def get(self, request):
        logout(request)
        redirect("login_page")


class LoginPage(View):
    def get(self, request):
        logout(request)
        redirect("login_page")


class RegisterPage(View):
    form_class = RegistrationForm
    template_name = "homepage/wannain.html"

    def get_invite_slug_from_db(self, invite_slug: str):
        try:
            return InviteLinkList.objects.get(slug=invite_slug)
        except ObjectDoesNotExist:
            return None

    def get(self, request, invite_slug):
        if not self.get_invite_slug_from_db(invite_slug):
            return HttpResponseForbidden()
        registration_form = self.form_class()
        return render(request, self.template_name, context={"form": registration_form})

    def post(self, request, invite_slug):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            user = bound_form.save(commit=False)
            password = bound_form.cleaned_data["password"]
            username = bound_form.cleaned_data["username"]
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    self.get_invite_slug_from_db(invite_slug).delete()
                    return redirect()
        return render(request, self.template_name, context={"form": bound_form})


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
