import hashlib
from typing import Any

from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, CreateView
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

from .models import CustomUser, Room, Taikyoku3, Taikyoku4, Senseki3, Senseki4
from .form import SignUpForm, RoomForm

class Home(TemplateView):
    template_name = "PunPals/home.html"

def SignUp(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            CustomUser.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                )
            return redirect('login')
    else:
        form = SignUpForm()

    return render(request, 'PunPals/signup.html', {'form': form})

class Login(LoginView):
    template_name="PunPals/login.html"

    def get_success_url(self):
        url = reverse('user_home', args=[self.request.user.username]) 
        return url
    
class Logout(LogoutView):
    next_page = reverse_lazy('home')

class UserDispatchMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.username != kwargs.get('username'):
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

class UserHome(UserDispatchMixin, TemplateView, LoginRequiredMixin):
    template_name = "PunPals/user_home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        context['username'] = username
        return context
    
class CreateRoom(UserDispatchMixin, CreateView, LoginRequiredMixin):
    template_name = "PunPals/create_room.html"
    model = Room
    form_class = RoomForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        password = form.cleaned_data['passwd']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        form.instance.passwd = hashed_password

        instance = form.save()

        user = get_user_model().objects.get(username=self.request.user.username)
        instance.users.add(user)

        return HttpResponseRedirect(reverse('room_home', args=[self.request.user.username, instance.name]))

class JoinRoom(UserDispatchMixin, TemplateView):
    template_name = "PunPals/join_room.html"

class RoomHome(UserDispatchMixin, TemplateView):
    template_name = "PunPals/room_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        roomname = self.kwargs.get('roomname')
        context['roomname'] = roomname
        return context