from rest_framework import generics
from rest_framework import viewsets
from .serializers import PostSerializer
from .models import Post
from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework.response import Response


class GetPostViewSet(mixins.RetrieveModelMixin,
                     mixins.CreateModelMixin,
                     generics.GenericAPIView):
    @classmethod
    def get_extra_actions(cls):
        return []

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class CreatePostViewSet(generics.CreateAPIView):

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @classmethod
    def get_extra_actions(cls):
        return []

    # def post(self, request, *args, **kwargs):
    #     return self.retrieve(request, *args, **kwargs)

