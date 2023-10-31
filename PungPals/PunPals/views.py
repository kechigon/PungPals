from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render

from .models import User, Room, Taikyoku3, Taikyoku4, Senseki3, Senseki4

class Home(TemplateView):
    template_name = "PunPals/home.html"