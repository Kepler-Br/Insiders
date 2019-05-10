from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('user/<str:user_slug>', login_required(views.UserHomepage.as_view()), name="user_home"),
    path('user/<str:user_id>/posts', login_required(views.UserPosts.as_view()), name="user_posts"),
    path('post/tags', login_required(views.view_post_tags), name="post_tag_list"),
    path('post/new', login_required(views.PostCreate.as_view()), name="post_create"),
    path('post/<str:slug>', login_required(views.ViewPost.as_view()), name="post_detail_url"),
    path('home', login_required(views.CurrentUserHomepage.as_view()), name="homepage"),
    path('home/edit', login_required(views.UserHomepageEdit.as_view()), name="homepage_edit"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
