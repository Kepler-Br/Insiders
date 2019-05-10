from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('invite/<str:invite_slug>', views.RegistrationPage.as_view(), name="register_page"),
    path('request_invite', views.RequestInvitePage.as_view(), name="request_invite_page"),
    path('logout', login_required(views.LogoutPage.as_view()), name="logout_page"),
    path('login', auth_views.LoginView.as_view(template_name="UserAuthApp/login.html"), name="login_page"),
    path('home/edit', login_required(views.UserHomepageEdit.as_view()), name="homepage_edit"),
    path('user/<str:user_slug>', login_required(views.UserHomepage.as_view()), name="user_home"),
    path('home', login_required(views.CurrentUserHomepage.as_view()), name="homepage"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)