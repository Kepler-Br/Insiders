"""insiders URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.generic import TemplateView
from .views import RootAddress

urlpatterns = [
    path('api/', include('blog.api.urls')),
    path('api/', include('users.api.urls')),

    path('', RootAddress.as_view(), name="index"),
    path('about/', TemplateView.as_view(template_name='about.html'), name="about_page"),
    path('', include('blog.urls')),
    path('', include('bookmarks.urls')),
    path('', include('users.urls')),
    path('admin/', admin.site.urls),
    # path('', RedirectView.as_view(pattern_name='user_home', permanent=False, initkwargs={"user_slug": }), name="root_address"),
]


