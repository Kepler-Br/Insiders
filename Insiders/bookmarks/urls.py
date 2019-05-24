from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('user/<str:slug>/bookmarks', views.UserBookmarksFolders.as_view(), name="user_bookmark_folders"),

    path('bookmarks/create-folder', views.CreateBookmarkFolder.as_view(), name="user_bookmark_folder_create"),
    path('bookmarks/folder/<str:slug>/delete', views.DeleteBookmarkFolder.as_view(), name="bookmark_folder_delete"),
    path('bookmarks/folder/<str:slug>/edit', views.EditBookmarkFolder.as_view(), name="bookmark_folder_edit"),
    path('bookmarks/folder/<str:slug>', views.ViewBookmarkFolder.as_view(), name="bookmark_folder"),

    path('bookmarks/create-bookmark', views.CreateBookmark.as_view(), name="user_bookmark_create"),
    path('bookmarks/bookmark/<str:slug>/delete', views.DeleteBookmark.as_view(), name="bookmark_delete"),
    path('bookmarks/bookmark/<str:slug>/edit', views.EditBookmark.as_view(), name="bookmark_edit"),
    path('bookmarks/bookmark/<str:slug>', views.ViewBookmark.as_view(), name="bookmark"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)