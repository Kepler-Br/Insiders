from django.urls import path
from . import views

urlpatterns = [
    path('posts', views.PostRudView.as_view(), name="api_post"),
]

