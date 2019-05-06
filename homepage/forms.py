from django.core.exceptions import ValidationError
from .models import *
from django import forms
from django.utils.text import slugify
import time
import base64


class MultiValueTextWidget(forms.TextInput):
    def _get_value(self, value):
        return " ".join(value)

    def _format_value(self, value):
        if self.is_localized:
            return formats.localize_input(self._get_value(value))
        return self._get_value(value)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "slug", "body", "post_tags"]

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Post title'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Post URL'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Post body'}),
            'post_tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Post tags'}),
        }

    def __init__(self, *args, **kwargs):

        # print(dir(self.fields['post_tags']))
        # self.fields['post_tags'] = args['post_tags']
        print(args[0]["post_tags"])
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['slug'].required = False
        self.fields['post_tags'].required = False

    def clean_slug(self):
        new_slug = slugify(self.cleaned_data['slug'])
        timestamp = int(time.time()*1e6)
        timestamp_bytes = timestamp.to_bytes((timestamp.bit_length() + 7) // 8, byteorder='big')
        timestamp_base64_str = base64.b64encode(timestamp_bytes).decode('utf-8').replace('=', '')
        if len(new_slug) == 0:
            return timestamp_base64_str
        else:
            return f"{new_slug}-{timestamp_base64_str}"

    def clean_post_tags(self):
        hashtags = self.cleaned_data['post_tags']
        if len(hashtags) == 0:
            return hashtags
        for hashtag in hashtags.split(' '):
            print(hashtag)
        raise ValidationError("Tag is not correct.")
        if '#' not in tags:
            raise ValidationError("Tag is not correct.")
