from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
# from django.views.generic import RedirectView


urlpatterns = [
    path('users/<int:pk>', views.ProfileRudView.as_view(), name="api_profiles"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
