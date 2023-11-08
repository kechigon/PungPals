from django.views.generic import TemplateView
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy

from .models import CustomUser, Room, Taikyoku3, Taikyoku4, Senseki3, Senseki4
from .form import SignUpForm

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
    redirect_authenticated_user=True,
    template_name="PunPals/login.html"

    def get_success_url(self):
        url = reverse('user_home', args=[self.request.user.username]) 
        return url
    
class Logout(LogoutView):
    next_page = reverse_lazy('home')

class UserHome(TemplateView, LoginRequiredMixin):
    template_name = "PunPals/user_home.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.username != kwargs.get('username'):
            return HttpResponseForbidden("このページを閲覧できません")
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        context['username'] = username
        return context