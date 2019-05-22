from .models import *
from django import forms
from django.utils.text import slugify
import time
import base64


class BookmarkFolderForm(forms.ModelForm):
    title = forms.CharField(label="Folder title",
                                  widget=forms.TextInput(
                                      attrs={'class': 'form-control', 'placeholder': 'Folder description'}))

    description = forms.CharField(label="Folder description:",
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Folder description'}))

    is_hidden = forms.BooleanField(label="Hide folder from others.",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), required=False)

    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    image = forms.FileField(widget=forms.FileInput(),
                            required=False)

    class Meta:
        model = BookmarkFolder
        fields = ["title", "image", "slug", "description", "is_hidden"]

    def clean_slug(self):
        timestamp = int(time.time()*1e6)
        timestamp_bytes = timestamp.to_bytes((timestamp.bit_length() + 7) // 8, byteorder='big')
        timestamp_base64_str = base64.b64encode(timestamp_bytes).decode('utf-8').replace('=', '')
        return timestamp_base64_str


class BookmarkForm(forms.ModelForm):
    title = forms.CharField(label="Bookmark title",
                                  widget=forms.TextInput(
                                      attrs={'class': 'form-control', 'placeholder': 'Bookmark description'}))
    body = forms.CharField(label="Bookmark body",
                                  widget=forms.Textarea(
                                      attrs={'class': 'form-control', 'placeholder': 'Bookmark body'}))

    tags = forms.CharField(label="Bookmark tags",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bookmark tags'}), required=False)

    is_hidden = forms.BooleanField(label="Hide bookmark from others.",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), required=False)

    folder = forms.ChoiceField(widget=forms.SelectMultiple(attrs={'class': 'form-control'}))

    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    image = forms.FileField(widget=forms.FileInput(), required=False)

    class Meta:
        model = Bookmark
        fields = ["title", "body", "image", "slug", "folder", "tags", "is_hidden"]

    def clean_slug(self):
        timestamp = int(time.time()*1e6)
        timestamp_bytes = timestamp.to_bytes((timestamp.bit_length() + 7) // 8, byteorder='big')
        timestamp_base64_str = base64.b64encode(timestamp_bytes).decode('utf-8').replace('=', '')
        return timestamp_base64_str
