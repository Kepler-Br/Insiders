from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('invite/<str:invite_slug>', views.RegistrationPage.as_view(), name="register_page"),
    path('request_invite', views.RequestInvitePage.as_view(), name="request_invite_page"),
    path('logout', login_required(views.LogoutPage.as_view()), name="logout_page"),
    path('login', auth_views.LoginView.as_view(template_name="UserAuthApp/login.html"), name="login_page"),
]
