from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from .forms import *
from .models import *
from django.http import HttpResponseForbidden
from homepage.models import Post

# Create your views here.


class LogoutPage(View):
    def get(self, request):
        logout(request)
        return redirect("login_page")


class RequestInvitePage(View):
    form_class = RequestInviteForm
    template_name = "users/request_invite.html"
    success_template_name = "users/request_submitted.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("homepage")
        form = self.form_class()
        return render(request, self.template_name, context={"form": form})

    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            bound_form.save()
            return render(request, self.success_template_name, context={"form": bound_form})
        return render(request, self.template_name, context={"form": bound_form})


class RegistrationPage(View):
    form_class = RegistrationForm
    template_name = "users/registration.html"
    submitted_template = "users/request_submitted.html"

    def get_invite_slug_from_db(self, invite_slug: str):
        try:
            return InviteLinkList.objects.get(slug=invite_slug)
        except ObjectDoesNotExist:
            return None

    def get(self, request, invite_slug):
        if request.user.is_authenticated:
            return redirect("homepage")
        # if not self.get_invite_slug_from_db(invite_slug):
        #     return HttpResponseForbidden()
        registration_form = self.form_class()
        return render(request, self.template_name, context={"form": registration_form})

    def post(self, request, invite_slug):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            bound_form.save()
            return render(request, self.submitted_template)
            # password = bound_form.cleaned_data["password"]
            # username = bound_form.cleaned_data["username"]
            # user.set_password(password)
            # user.save()

            # user = authenticate(username=username, password=password)
            # if user is not None:
            #     if user.is_active:
            #         login(request, user)
                    # self.get_invite_slug_from_db(invite_slug).delete()

        return render(request, self.template_name, context={"form": bound_form})


class UserHomepageEdit(View):
    template_name = "users/homepage_edit.html"

    def get(self, request):
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        context = {"user_form": user_form,
                   "profile_form": profile_form}
        return render(request, self.template_name, context=context)

    def post(self, request):
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect("homepage")
        else:
            context = {"user_form": user_form,
                       "profile_form": profile_form}
            return render(request, self.template_name, context=context)


class CurrentUserHomepage(View):
    def get(self, request):
        posts = Post.objects.filter(author=request.user).order_by('-date_pub')
        count = {"posts": Post.objects.count()}
        context = {"posts": posts, "profile": request.user.profile, "media_count": count}
        return render(request, "users/homepage.html", context=context)


class UserHomepage(View):
    def get(self, request, user_slug):
        user = User.objects.get(username=user_slug)
        posts = Post.objects.filter(author=user).order_by('-date_pub')
        count = {"posts": Post.objects.count()}
        context = {"posts": posts, "profile": user.profile, "media_count": count}
        return render(request, "users/homepage.html", context=context)

