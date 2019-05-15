from .models import *
from django import forms
from django.utils.text import slugify
import time
import base64

title = models.TextField(max_length=100, db_index=True)
description = models.TextField(max_length=1000, db_index=True)
slug = models.SlugField(max_length=20)
author = models.ForeignKey(User, on_delete=models.CASCADE)
is_hidden = models.BooleanField(default=False)


class CreateBookmarkFolderForm(forms.ModelForm):
    title = forms.CharField(label="Folder title",
                                  widget=forms.TextInput(
                                      attrs={'class': 'form-control', 'placeholder': 'Folder description'}))

    description = forms.CharField(label="Folder description:",
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Folder description'}))

    is_hidden = forms.BooleanField(label="Hide folder from others.",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), required=False)

    slug = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model = BookmarkFolder
        fields = ["title", "slug", "description", "is_hidden"]

    def __init__(self, *args, **kwargs):
        super(CreateBookmarkFolderForm, self).__init__(*args, **kwargs)
        self.fields['slug'].required = False

    def clean_slug(self):
        timestamp = int(time.time()*1e6)
        timestamp_bytes = timestamp.to_bytes((timestamp.bit_length() + 7) // 8, byteorder='big')
        timestamp_base64_str = base64.b64encode(timestamp_bytes).decode('utf-8').replace('=', '')
        return timestamp_base64_str
