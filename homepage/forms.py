from django.core.exceptions import ValidationError
from .models import *
from django import forms
from django.utils.text import slugify
import time
import base64
import re
from django.utils.html import escape


class PostBodyForm(forms.Textarea):
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

    @staticmethod
    def get_single_tags_from_text(text: str) -> list:
        return re.findall(r"(\[\w+[ \w=\-\?\.:\/\"%]*\/\])", text)

    @staticmethod
    def get_attrs_from_tag(pattern: str, tag: str) -> dict:
        found = re.search(pattern, tag)
        if found:
            return found.groupdict()
        else:
            return {}

    def process_youtube_tag(self, youtube_tag: str):
        href_attr = self.get_attrs_from_tag(r"href=(https?:\/\/)?(www\.)?youtube\.com\/watch\?v=(?P<link>\w+)",
                                            youtube_tag)
        video_link = ""
        if href_attr:
            video_link = href_attr["link"]
        else:
            return youtube_tag

        style = ""
        size_attr = self.get_attrs_from_tag(r"size=(?P<size_num>\d+)(?P<size_units>px|%)", youtube_tag)
        if size_attr:
            style += f"""width: {size_attr["size_num"]}{size_attr["size_units"]};"""


        return f"""<div class="embed-responsive embed-responsive-4by3" style="{style}">
           <iframe class="embed-responsive-item" src="https://www.youtube.com/embed/{video_link}"></iframe>
           </div>"""

    @staticmethod
    def escape_html_tags(text: str) -> str:
        return text.replace("<", "&lt;").replace(">", "&gt;").replace("\'", "&#39;").replace("\"", "&quot;")\
            .replace("&", "&amp;")

    def clean_body(self):
        new_body = escape(self.cleaned_data['body'])
        single_tags = self.get_single_tags_from_text(new_body)
        for tag in single_tags:
            if "[youtube" in tag:
                processed_tag = self.process_youtube_tag(tag)
                new_body = \
                    new_body.replace(tag, processed_tag)
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
