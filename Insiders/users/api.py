from .models import Profile
from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from .serializers import ProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = ProfileSerializer

    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        user = User.objects.get(username=username)
        return Profile.objects.get(user=user)

