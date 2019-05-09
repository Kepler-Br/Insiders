from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from .forms import *
from .models import *
from django.http import HttpResponseForbidden

# Create your views here.


class LogoutPage(View):
    def get(self, request):
        logout(request)
        redirect("login_page")


class LoginPage(View):
    def get(self, request):
        logout(request)
        redirect("login_page")


class RequestInvitePage(View):
    form_class = RequestInviteForm
    template_name = "UserAuthApp/request_invite.html"
    success_template_name = "UserAuthApp/request_submitted.html"

    def get(self, request):
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
    # template_name = "UserAuthApp/registration.html"
    # template_name = "UserAuthApp/request_submitted.html"

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
