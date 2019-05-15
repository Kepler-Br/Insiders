from django.urls import path
from . import views


urlpatterns = [
    path('user/<str:user_slug>/bookmarks', views.UserBookmarksFolders.as_view(), name="user_bookmark_folders"),
    path('bookmarks/create', views.CreateBookmarkFolder.as_view(), name="user_bookmark_folder_create"),
]
