from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, CreateView

from .models import User, Room, Taikyoku3, Taikyoku4, Senseki3, Senseki4

class Home(TemplateView):
    template_name = "PunPals/home.html"

class SignUp(CreateView):
    template_name = "PunPals/signup.html"

class UserHome(ListView):
    template_name = "PunPals/user_home.html"