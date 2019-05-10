from django import forms
from django.contrib.auth.models import User
from .models import InviteRequests, Profile
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]





class RequestInviteForm(forms.ModelForm):
    class Meta:
        model = InviteRequests
        fields = ["username", "firstname", "secondname", "contacts", "about"]

        widgets = {
            "username": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            "firstname": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}),
            "secondname": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Second name'}),
            "contacts": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contacts'}),
            "about": forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'About you'}),
        }


class UserEditForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["image", "short_about", "status", "gender"]
