from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('invite/<str:invite_slug>', views.RegisterPage.as_view(), name="getting_inside"),
    path('logout', views.LogoutPage.as_view(), name="logout_page"),
    path('login', views.LoginPage.as_view(), name="login_page"),
    path('user/<str:user_slug>', views.UserHomepage.as_view(), name="user_home"),
    path('user/<str:user_id>/posts', views.UserPosts.as_view(), name="user_posts"),
    path('post/tags', views.view_post_tags, name="post_tag_list"),
    path('post/new', views.PostCreate.as_view(), name="post_create"),
    path('post/<str:slug>', views.ViewPost.as_view(), name="post_detail_url"),
]
