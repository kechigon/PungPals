from django.urls import path

from . import views

urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("signup", views.SignUp.as_view(), name="signup"),
    path("user_home", views.UserHome.as_view(), name="user_home"),
]