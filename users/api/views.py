from rest_framework import generics
from .serializers import ProfileSerializer
from users.models import Profile

class ProfileRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.all()
