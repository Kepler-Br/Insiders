from django.core.exceptions import ValidationError
from .models import *
from django import forms
from django.utils.text import slugify
import time
import base64
import re


class CommentForm(forms.Widget):
    input_type = 'select'  # Subclasses must define this.
    template_name = 'django/forms/widgets/text.html'

    def __init__(self, attrs=None):
        if attrs is not None:
            attrs = attrs.copy()
            self.input_type = attrs.pop('type', self.input_type)
        super().__init__(attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['type'] = self.input_type
        return context


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "slug", "body"]

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Post title'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Post URL'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Post body'}),
        }

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['slug'].required = False

    def clean_slug(self):
        new_slug = slugify(self.cleaned_data['slug'])
        timestamp = int(time.time()*1e6)
        timestamp_bytes = timestamp.to_bytes((timestamp.bit_length() + 7) // 8, byteorder='big')
        timestamp_base64_str = base64.b64encode(timestamp_bytes).decode('utf-8').replace('=', '')
        if len(new_slug) == 0:
            return timestamp_base64_str
        else:
            return f"{new_slug}-{timestamp_base64_str}"

    def process_youtube_tag(self, body: str):


    def clean_body(self):
        new_body = self.cleaned_data['body']
        new_body += """<div class="embed-responsive embed-responsive-4by3">
                       <iframe class="embed-responsive-item" src="..."></iframe>
                       </div>"""
        return new_body

    # def clean_post_tags(self):
    #     print(self.cleaned_data['post_tags'])
    #     # hashtags = self.cleaned_data['post_tags']
    #     # if len(hashtags) == 0:
    #     #     return hashtags
    #     # for hashtag in hashtags.split(' '):
    #     #     print(hashtag)
    #     raise ValidationError("Tag is not correct.")
    #     if '#' not in tags:
    #         raise ValidationError("Tag is not correct.")
