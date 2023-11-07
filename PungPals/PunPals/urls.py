from django.contrib.auth.views import LoginView
from django.urls import path

from . import views

urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("signup", views.SignUp, name="signup"),
    path("login", LoginView.as_view(
        redirect_authenticated_user=False,
        template_name="PunPals/login.html"
    ), name="login"),
    path("user_home", views.UserHome.as_view(), name="user_home"),
]