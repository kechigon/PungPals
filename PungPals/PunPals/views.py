import hashlib

from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, CreateView, DeleteView
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.views import View

from .models import CustomUser, Room, Taikyoku3, Taikyoku4, Senseki3, Senseki4
from .form import SignUpForm, CreateRoomForm, JoinRoomForm

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
        user = CustomUser.objects.get(username=username)
        context['username'] = username
        context['user_rooms'] = user.room_set.all()
        return context

class DeleteRoom(UserDispatchMixin, DeleteView, LoginRequiredMixin):
    model = Room

    def get_success_url(self):
        return reverse('user_home', args=[self.request.user.username])

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())
    
class FormKwargsMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    
class CreateRoom(UserDispatchMixin, FormKwargsMixin, CreateView, LoginRequiredMixin):
    template_name = "PunPals/create_room.html"
    model = Room
    form_class = CreateRoomForm

    def form_valid(self, form):
        password = form.cleaned_data['passwd']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        form.instance.passwd = hashed_password

        instance = form.save()

        user = get_user_model().objects.get(username=self.request.user.username)
        instance.users.add(user)

        return HttpResponseRedirect(reverse('room_home', args=[self.request.user.username, instance.name]))

class JoinRoom(UserDispatchMixin, FormKwargsMixin, View, LoginRequiredMixin):
    template_name = "PunPals/join_room.html"

    def get(self, request, *args, **kwargs):
        form = JoinRoomForm(request=request)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = JoinRoomForm(request.POST, request=request)
        if form.is_valid():
            roomname = form.cleaned_data.get('roomname')
            password = form.cleaned_data.get('password')
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            room = Room.objects.filter(name=roomname, passwd=hashed_password).first()

            if room is None:
                form.add_error(None, '部屋名またはパスワードが違います')
            else:
                room.users.add(request.user)
                room.save()
                return HttpResponseRedirect(reverse('room_home', args=[request.user.username, roomname]))
            
        return render(request, self.template_name, {'form': form})

class RoomHome(UserDispatchMixin, TemplateView):
    template_name = "PunPals/room_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        roomname = self.kwargs.get('roomname')
        context['roomname'] = roomname
        return context