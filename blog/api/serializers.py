from rest_framework import serializers

from blog.models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "slug",
            "title",
            "body",
            "short_body",
            "post_tags",
            "date_pub",
        ]
