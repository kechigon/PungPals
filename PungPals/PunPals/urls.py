from django.urls import path

from . import views

urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("signup/", views.SignUp, name="signup"),
    path("login/", views.Login.as_view(), name="login"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path("<str:username>/", views.UserHome.as_view(), name="user_home"),
    path("<str:username>/create_room/", views.CreateRoom.as_view(), name="create_room"),
]