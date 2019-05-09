from django.urls import path
from . import views

urlpatterns = [
    path('invite/<str:invite_slug>', views.RegistrationPage.as_view(), name="register_page"),
    path('request_invite', views.RequestInvitePage.as_view(), name="request_invite_page"),
    path('logout', views.LogoutPage.as_view(), name="logout_page"),
    path('login', views.LoginPage.as_view(), name="login_page"),
]
