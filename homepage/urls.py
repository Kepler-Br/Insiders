from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('getting_inside', views.RegistrationRequest.as_view(), name="getting_inside"),
    path('user/<str:user_slug>', views.UserHomepage.as_view(), name="user_home"),
    path('user/<str:user_id>/posts', views.UserPosts.as_view(), name="user_posts"),
    path('post/tags', views.view_post_tags, name="post_tag_list"),
    path('post/<str:slug>', views.ViewPost.as_view(), name="post_detail_url"),
]
