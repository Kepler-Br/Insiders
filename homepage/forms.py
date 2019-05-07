from django.core.exceptions import ValidationError
from .models import *
from django import forms
from django.utils.text import slugify
import time
import base64
import re
from django.utils.html import escape


class TextareaWithTags(forms.Textarea):
    input_type = 'text'  # Subclasses must define this.
    template_name = 'django/forms/widgets/textarea.html'

    def __init__(self, attrs=None):
        if attrs is not None:
            attrs = attrs.copy()
            self.input_type = attrs.pop('type', self.input_type)
        super().__init__(attrs)

    def get_context(self, name, value, attrs):
        if value:
            value = self.process_single_tags(escape(value))
        context = super().get_context(name, value, attrs)
        context['widget']['type'] = self.input_type
        return context

    @staticmethod
    def process_single_tags(text: str) -> str:
        tags = TextareaWithTags.get_single_tags_from_text(text)
        for tag in tags:
            if "[youtube" in tag:
                processed = TextareaWithTags.process_youtube_tag(tag)
                text = text.replace(tag, processed)
        return text

    @staticmethod
    def process_youtube_tag(tag: str) -> str:
        attrs: dict = TextareaWithTags.get_attributes_from_tag(tag)
        href = attrs.get("href")
        if not href:
            return tag

        link_matched = re.match(r"(https?:\/\/)?(www\.)?youtube\.com\/watch\?v=(\w+)", href)
        if not link_matched:
            return tag
        video_link = link_matched[3]

        style = ""
        size_attr = attrs.get("size")
        if size_attr:
            size_match = re.match(r"(\d+)(px|%)", size_attr)
            if size_match:
                size_number = size_match[1]
                size_units = size_match[2]
                style += f"""width:{size_number}{size_units};"""

        return f"""<div class="embed-responsive embed-responsive-4by3" style="{style}">
               <iframe class="embed-responsive-item" src="https://www.youtube.com/embed/{video_link}"></iframe>
               </div>"""


    @staticmethod
    def get_single_tags_from_text(text: str) -> list:
        return re.findall(r"(\[\w+ [\w\d \/:=\?\.%\"]+\/\])", text)

    @staticmethod
    def get_attributes_from_tag(tag: str) -> dict:
        found = re.findall(r"(\w+)=\"([\w\d \/:=\?\.%]+)\"", tag)
        attributes = {}
        for key, value in found:
            attributes[key] = value
        return attributes



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "slug", "body"]

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Post title'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Post URL'}),
            'body': TextareaWithTags(attrs={'class': 'form-control', 'placeholder': 'Post body'}),
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
