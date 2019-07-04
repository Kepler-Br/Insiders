from rest_framework import routers
from .api import GetPostViewSet, CreatePostViewSet
from django.urls import path, include


# urlpatterns = router.urls()
# urlpatterns = [
#     path("api/post/get", GetPostViewSet.as_view())
# ]

# router = routers.SimpleRouter()
# router.register(r'api/post/get', GetPostViewSet, base_name="post_get")
# urlpatterns = router.urls

urlpatterns = [
    # path('', include(router.urls)),
    path('api/post/get/<int:pk>/', GetPostViewSet.as_view()),
    path('api/post/create/', CreatePostViewSet.as_view()),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]