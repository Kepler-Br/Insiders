from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('post/<str:slug>/edit', login_required(views.PostEdit.as_view()), name="post_edit"),
    path('post/<str:slug>/delete', login_required(views.PostDelete.as_view()), name="post_delete"),
    path('post/new', login_required(views.PostCreate.as_view()), name="post_create"),
    path('user/<str:user_id>/posts', login_required(views.UserPosts.as_view()), name="user_posts"),

    path('post/<str:slug>', login_required(views.ViewPost.as_view()), name="post_view"),

    # path('post/tags', login_required(views.view_post_tags), name="post_tag_list"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
