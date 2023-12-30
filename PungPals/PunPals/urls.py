from django.urls import path

from . import views

urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("signup/", views.SignUp, name="signup"),
    path("login/", views.Login.as_view(), name="login"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path("<str:username>/", views.UserHome.as_view(), name="user_home"),
    path("<str:username>/create_room/", views.CreateRoom.as_view(), name="create_room"),
    path("<str:username>/join_room/", views.JoinRoom.as_view(), name="join_room"),
    path("<str:username>/delete_room/<int:pk>/", views.DeleteRoom.as_view(), name="delete_room"),
    path("<str:username>/<str:roomname>/", views.RoomHome.as_view(), name="room_home"),
    path("<str:username>/<str:roomname>/register_result3", views.RegisterResult3.as_view(), name="register_result3"),
    path("<str:username>/<str:roomname>/register_result4", views.RegisterResult4.as_view(), name="register_result4"),
    path("<str:username>/<str:roomname>/delete_result3", views.DeleteResult3List.as_view(), name="delete_result3"),
    path("<str:username>/<str:roomname>/delete_taikyoku3/<int:pk>/", views.DeleteResult3.as_view(), name="delete_taikyoku3"),
    path("<str:username>/<str:roomname>/delete_result4", views.DeleteResult4List.as_view(), name="delete_result4"),
    path("<str:username>/<str:roomname>/delete_taikyoku4/<int:pk>/", views.DeleteResult4.as_view(), name="delete_taikyoku4"),
    path("<str:username>/<str:roomname>/ranking", views.Ranking.as_view(), name="ranking"),
]