from rest_framework import generics
from .serializers import PostSerializer
from blog.models import Post
from django.contrib.auth.models import User


class PostRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'slug'
    serializer_class = PostSerializer

    def get_queryset(self):
        username = self.request.GET.get("user")
        if username is not None:
            user = User.objects.get(username=username)
            result = Post.objects.filter(author=user)
            return result
        return Post.objects.all()
