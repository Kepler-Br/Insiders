from django import forms
from django.contrib.auth.models import User
from .models import InviteRequests


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "password", "first_name", "username"]

        widgets = {
            "email": forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}),
            "password": forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            "first_name": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Firstname'}),
            "username": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        }


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


class LoginForm(forms.Form):
    class Meta:
        fields = ["username", "password"]

        widgets = {
            "username": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username or email'}),
            "password": forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        }
