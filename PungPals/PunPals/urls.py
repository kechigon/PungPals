from django.urls import path

from . import views

urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("signup/", views.SignUp, name="signup"),
    path("login/", views.Login.as_view(), name="login"),
    path("<str:username>/", views.UserHome.as_view(), name="user_home"),
]