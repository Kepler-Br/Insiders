# from django.core.exceptions import ValidationError
from .models import *
from django import forms
from django.utils.text import slugify
import time
import base64
import re

from django.utils.html import escape


class SingleTagProcessor:
    @staticmethod
    def process(text: str) -> str:
        tags = SingleTagProcessor.get_single_tags_from_text(text)
        for tag in tags:
            if "[youtube" in tag:
                processed = SingleTagProcessor.process_youtube_tag(tag)
                text = text.replace(tag, processed)
        return text

    @staticmethod
    def process_youtube_tag(tag: str) -> str:
        attrs: dict = SingleTagProcessor.get_attributes_from_tag(tag)
        href = attrs.get("link")
        if not href:
            return tag

        link_matched = re.match(r"(https?:\/\/)?(www\.)?youtube\.com\/watch\?v=([\-_\w\d]+)", href)
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
        return re.findall(r"(\[\w+ [\w\d \/:=\?\.%\`_\-]+\/])", text)

    @staticmethod
    def get_attributes_from_tag(tag: str) -> dict:
        found = re.findall(r"(\w+)=\`([\w\d\-_ \/:=\?\.%]+)\`", tag)
        attributes = {}
        for key, value in found:
            attributes[key] = value
        return attributes


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "slug", "short_body", "body", "post_tags", "processed_body", "processed_short_body"]

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Post title'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Post URL (optional)'}),
            'short_body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Short post body (optional)'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Post body'}),
            'post_tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Post tags (optional)'}),
            'processed_body': forms.HiddenInput(),
            'processed_short_body': forms.HiddenInput(),
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

    def process_short_body(self):
        short_body = self.cleaned_data['short_body']
        if short_body:
            # self.cleaned_data['short_body'] = short_body
            new_short_body = escape(short_body)
            self.cleaned_data['processed_short_body'] = SingleTagProcessor.process(new_short_body).replace("\r\n", "<br>")
        else:
            self.cleaned_data['processed_short_body'] = short_body

    def process_body(self):
        body = self.cleaned_data['body']
        new_body = escape(body)
        # self.cleaned_data['body'] = new_body
        self.cleaned_data['processed_body'] = SingleTagProcessor.process(new_body).replace("\r\n", "<br>")

    def clean(self):
        super().clean()
        self.process_short_body()
        self.process_body()


class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "short_body", "body", "post_tags", "processed_body", "processed_short_body"]

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Post title'}),
            'short_body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Short post body (optional)'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Post body'}),
            'post_tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Post tags (optional)'}),
            'processed_body': forms.HiddenInput(),
            'processed_short_body': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super(PostEditForm, self).__init__(*args, **kwargs)

    def process_short_body(self):
        short_body = self.cleaned_data['short_body']
        if short_body:
            self.cleaned_data['short_body'] = short_body
            new_short_body = escape(short_body)
            self.cleaned_data['processed_short_body'] = SingleTagProcessor.process(new_short_body).replace("\r\n", "<br>")


    def process_body(self):
        body = self.cleaned_data['body']
        new_body = escape(body)
        # self.cleaned_data['body'] = body
        self.cleaned_data['processed_body'] = SingleTagProcessor.process(new_body).replace("\r\n", "<br>")
        print()

    def clean(self):
        super().clean()
        self.process_short_body()
        self.process_body()
