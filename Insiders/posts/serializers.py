from rest_framework import serializers
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class PostSerializer(serializers.ModelSerializer):
    # author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    serializers.ReadOnlyField(default=serializers.CurrentUserDefault())

    # def get_author(self, obj):
    #     return obj.author.username

    class Meta:
        model = Post
        fields = ["title", "slug", "body", "processed_body", \
                  "short_body", "processed_short_body", \
                  "post_tags", "date_pub", "author", "pk"]