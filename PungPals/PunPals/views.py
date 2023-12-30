import hashlib

from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, CreateView, DeleteView, ListView
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.views import View

from .models import CustomUser, Room, Taikyoku3, Taikyoku4, Senseki3, Senseki4
from .form import SignUpForm, CreateRoomForm, JoinRoomForm, Taikyoku3Form, Taikyoku4Form, RankingFilterForm

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

class UserHome(UserDispatchMixin, LoginRequiredMixin, TemplateView):
    template_name = "PunPals/user_home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        user = CustomUser.objects.get(username=username)
        context['username'] = username
        context['user_rooms'] = user.room_set.all()
        return context

class DeleteRoom(UserDispatchMixin, LoginRequiredMixin, DeleteView):
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
    
class CreateRoom(UserDispatchMixin, FormKwargsMixin, LoginRequiredMixin, CreateView):
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

class JoinRoom(UserDispatchMixin, FormKwargsMixin, LoginRequiredMixin, View):
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

class RoomDispatchMixin:
    def dispatch(self, request, *args, **kwargs):
        username = kwargs.get('username')
        roomname = kwargs.get('roomname')
        
        user = request.user
        room = get_object_or_404(Room, name=roomname)
        
        if not room.users.filter(id=user.id).exists():
            return HttpResponseRedirect(reverse('user_home', args=[username]))
        return super().dispatch(request, *args, **kwargs)

class RoomHome(UserDispatchMixin, RoomDispatchMixin, LoginRequiredMixin, TemplateView):
    template_name = "PunPals/room_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        roomname = self.kwargs.get('roomname')
        user = get_object_or_404(CustomUser, username=username)
        room = get_object_or_404(Room, name=roomname)

        senseki3 = Senseki3.objects.filter(user=user, room=room).first()
        senseki4 = Senseki4.objects.filter(user=user, room=room).first()

        context['room_users'] = room.users.all()
        context['username'] = username
        context['roomname'] = roomname
        context['senseki3'] = senseki3
        context['senseki4'] = senseki4
        return context
    
class RegisterResult3(UserDispatchMixin, RoomDispatchMixin, LoginRequiredMixin, CreateView):
    model = Taikyoku3
    form_class = Taikyoku3Form
    template_name = "PunPals/register_result3.html"

    def get_room(self):
        roomname = self.kwargs.get('roomname')
        return Room.objects.get(name=roomname)
    
    def form_valid(self, form):
        taikyoku3 = form.save(commit=False)
        taikyoku3.room = self.get_room()
        taikyoku3.save()

        ranking = taikyoku3.ranking()

        for index, (username, score) in enumerate(ranking):
            user = CustomUser.objects.get(username=username)
            senseki3, create = Senseki3.objects.get_or_create(user=user, room=taikyoku3.room)

            senseki3.gameNum += 1
            senseki3.scoreSum += score

            if index == 0:
                senseki3.firstNum += 1
            elif index == 1:
                senseki3.secondNum += 1
            elif index == 2:
                senseki3.thirdNum += 1
            if score < 0:
                senseki3.outNum += 1

            senseki3.rankMean = (1 * senseki3.firstNum + 2 * senseki3.secondNum + 3 * senseki3.thirdNum) / float(senseki3.gameNum)
            senseki3.firstRate = senseki3.firstNum / float(senseki3.gameNum)
            senseki3.secondRate = senseki3.secondNum / float(senseki3.gameNum)
            senseki3.thirdRate = senseki3.thirdNum / float(senseki3.gameNum)
            senseki3.outRate = senseki3.outNum / float(senseki3.gameNum)
            senseki3.scoreMean = senseki3.scoreSum / float(senseki3.gameNum)

            senseki3.save()

        return super().form_valid(form)
    
    def get_success_url(self):
        room = self.get_room()
        return reverse('register_result3', kwargs={'username': self.request.user.username, 'roomname': room.name})

    def get_form_kwargs(self):
        kwargs = super(RegisterResult3, self).get_form_kwargs()
        roomname = self.kwargs.get('roomname')
        kwargs['roomname'] = roomname
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.kwargs.get('username')
        context['roomname'] = self.kwargs.get('roomname')
        return context
    
class RegisterResult4(UserDispatchMixin, RoomDispatchMixin, LoginRequiredMixin, CreateView):
    model = Taikyoku4
    form_class = Taikyoku4Form
    template_name = "PunPals/register_result4.html"

    def get_room(self):
        roomname = self.kwargs.get('roomname')
        return Room.objects.get(name=roomname)
    
    def form_valid(self, form):
        taikyoku4 = form.save(commit=False)
        taikyoku4.room = self.get_room()
        taikyoku4.save()

        ranking = taikyoku4.ranking()

        for index, (username, score) in enumerate(ranking):
            user = CustomUser.objects.get(username=username)
            senseki4, create = Senseki4.objects.get_or_create(user=user, room=taikyoku4.room)

            senseki4.gameNum += 1
            senseki4.scoreSum += score

            if index == 0:
                senseki4.firstNum += 1
            elif index == 1:
                senseki4.secondNum += 1
            elif index == 2:
                senseki4.thirdNum += 1
            elif index == 3:
                senseki4.fourthNum += 1
            if score < 0:
                senseki4.outNum += 1

            senseki4.rankMean = (1 * senseki4.firstNum + 2 * senseki4.secondNum + 3 * senseki4.thirdNum + senseki4.fourthNum) / float(senseki4.gameNum)
            senseki4.firstRate = senseki4.firstNum / float(senseki4.gameNum)
            senseki4.secondRate = senseki4.secondNum / float(senseki4.gameNum)
            senseki4.thirdRate = senseki4.thirdNum / float(senseki4.gameNum)
            senseki4.fourthRate = senseki4.fourthNum / float(senseki4.gameNum)
            senseki4.outRate = senseki4.outNum / float(senseki4.gameNum)
            senseki4.scoreMean = senseki4.scoreSum / float(senseki4.gameNum)

            senseki4.save()

        return super().form_valid(form)
    
    def get_success_url(self):
        room = self.get_room()
        return reverse('register_result4', kwargs={'username': self.request.user.username, 'roomname': room.name})

    def get_form_kwargs(self):
        kwargs = super(RegisterResult4, self).get_form_kwargs()
        roomname = self.kwargs.get('roomname')
        kwargs['roomname'] = roomname
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.kwargs.get('username')
        context['roomname'] = self.kwargs.get('roomname')
        return context

class DeleteResult3List(UserDispatchMixin, RoomDispatchMixin, LoginRequiredMixin, ListView):
    model = Taikyoku3
    template_name = "PunPals/delete_result3.html"
    context_object_name = 'taikyoku3_list'

    def get_queryset(self):
        roomname = self.kwargs.get('roomname')
        room = get_object_or_404(Room, name=roomname)
        return Taikyoku3.objects.filter(room=room).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.kwargs.get('username')
        context['roomname'] = self.kwargs.get('roomname')
        return context

class DeleteResult3(UserDispatchMixin, RoomDispatchMixin, LoginRequiredMixin, DeleteView):
    model = Taikyoku3
    pk_url_kwarg = 'pk'

    def form_valid(self, form):
        self.object = self.get_object()
        ranking = self.object.ranking()
        
        # Update each user's results (Senseki3)
        for index, (username, score) in enumerate(ranking):
            user = CustomUser.objects.get(username=username)
            senseki = Senseki3.objects.get(user=user, room=self.object.room)
            if index == 0:
                senseki.firstNum -= 1
            elif index == 1: 
                senseki.secondNum -= 1
            elif index == 2:
                senseki.thirdNum -= 1
            
            if score < 0: 
                senseki.outNum -= 1
            
            senseki.gameNum -= 1
            senseki.scoreSum -= score

            if senseki.gameNum > 0:
                senseki.rankMean = (1 * senseki.firstNum + 2 * senseki.secondNum + 3 * senseki.thirdNum) / float(senseki.gameNum)
                senseki.firstRate = senseki.firstNum / float(senseki.gameNum)
                senseki.secondRate = senseki.secondNum / float(senseki.gameNum)
                senseki.thirdRate = senseki.thirdNum / float(senseki.gameNum)
                senseki.outRate = senseki.outNum / float(senseki.gameNum)
                senseki.scoreMean = senseki.scoreSum / float(senseki.gameNum)
            else:
                senseki.rankMean = 0
                senseki.firstRate = 0
                senseki.secondRate = 0
                senseki.thirdRate = 0
                senseki.outRate = 0
                senseki.scoreMean = 0

            senseki.save()

        response = super(DeleteResult3, self).form_valid(form)
        
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        username = self.kwargs.get('username')
        roomname = self.kwargs.get('roomname')
        return reverse_lazy('delete_result3', kwargs={'username': username, 'roomname': roomname})
    

class DeleteResult4List(UserDispatchMixin, RoomDispatchMixin, LoginRequiredMixin, ListView):
    model = Taikyoku4
    template_name = "PunPals/delete_result4.html"
    context_object_name = 'taikyoku4_list'

    def get_queryset(self):
        roomname = self.kwargs.get('roomname')
        room = get_object_or_404(Room, name=roomname)
        return Taikyoku4.objects.filter(room=room).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.kwargs.get('username')
        context['roomname'] = self.kwargs.get('roomname')
        return context

class DeleteResult4(UserDispatchMixin, RoomDispatchMixin, LoginRequiredMixin, DeleteView):
    model = Taikyoku4
    pk_url_kwarg = 'pk'

    def form_valid(self, form):
        self.object = self.get_object()
        ranking = self.object.ranking()
        
        # Update each user's results (Senseki4)
        for index, (username, score) in enumerate(ranking):
            user = CustomUser.objects.get(username=username)
            senseki = Senseki4.objects.get(user=user, room=self.object.room)
            if index == 0:
                senseki.firstNum -= 1
            elif index == 1: 
                senseki.secondNum -= 1
            elif index == 2:
                senseki.thirdNum -= 1
            elif index == 3:
                senseki.fourthNum -= 1

            
            if score < 0: 
                senseki.outNum -= 1
            
            senseki.gameNum -= 1
            senseki.scoreSum -= score

            if senseki.gameNum > 0:
                senseki.rankMean = (1 * senseki.firstNum + 2 * senseki.secondNum + 3 * senseki.thirdNum + 4 * senseki.fourthNum) / float(senseki.gameNum)
                senseki.firstRate = senseki.firstNum / float(senseki.gameNum)
                senseki.secondRate = senseki.secondNum / float(senseki.gameNum)
                senseki.thirdRate = senseki.thirdNum / float(senseki.gameNum)
                senseki.fourthRate = senseki.fourthNum / float(senseki.gameNum)
                senseki.outRate = senseki.outNum / float(senseki.gameNum)
                senseki.scoreMean = senseki.scoreSum / float(senseki.gameNum)
            else:
                senseki.rankMean = 0
                senseki.firstRate = 0
                senseki.secondRate = 0
                senseki.thirdRate = 0
                senseki.fourthNum = 0
                senseki.outRate = 0
                senseki.scoreMean = 0

            senseki.save()

        response = super(DeleteResult4, self).form_valid(form)
        
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        username = self.kwargs.get('username')
        roomname = self.kwargs.get('roomname')
        return reverse_lazy('delete_result4', kwargs={'username': username, 'roomname': roomname})
    
class Ranking(UserDispatchMixin, RoomDispatchMixin, LoginRequiredMixin, View):
    template_name = "PunPals/ranking.html"

    def get(self, request, *args, **kwargs):
        form = RankingFilterForm()
        context = {'form': form, 'username': kwargs['username'], 'roomname': kwargs['roomname']}
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        form = RankingFilterForm(request.POST)
        if form.is_valid():
            game_type = form.cleaned_data['game_type']
            game_num = form.cleaned_data['game_num']
            sort_by = form.cleaned_data['sort_by']
            print(sort_by)

            room = get_object_or_404(Room, name=kwargs['roomname'])

            if sort_by == 'rankMean':
                if game_type == 'senseki3':
                    senseki = Senseki3.objects.filter(room=room, gameNum__gte=game_num).order_by(sort_by)
                else:
                    senseki = Senseki4.objects.filter(room=room, gameNum__gte=game_num).order_by(sort_by)
            else:
                if game_type == 'senseki3':
                    senseki = Senseki3.objects.filter(room=room, gameNum__gte=game_num).order_by(f'-{sort_by}')
                else:
                    senseki = Senseki4.objects.filter(room=room, gameNum__gte=game_num).order_by(f'-{sort_by}')

            context = {
                'form': form,
                'senseki_list': senseki,
                'username': kwargs['username'],
                'roomname': kwargs['roomname'],
                'sort_by': sort_by
            }
            return render(request, self.template_name, context)
        else:
            context = {
                'form': form, 
                'username': kwargs['username'], 
                'roomname': kwargs['roomname']}
            return render(request, self.template_name, context)