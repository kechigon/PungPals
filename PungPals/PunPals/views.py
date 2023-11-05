from django.views.generic import TemplateView, ListView
from django.shortcuts import render, redirect
import hashlib

from .models import User, Room, Taikyoku3, Taikyoku4, Senseki3, Senseki4
from .form import SignUpForm

class Home(TemplateView):
    template_name = "PunPals/home.html"

def SignUp(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User(
                name=form.cleaned_data['username'],
                passwd=hashlib.sha256(form.cleaned_data['password1'].encode()).hexdigest(),
            )
            user.save()
            return redirect('login')
    else:
        form = SignUpForm()

    return render(request, 'PunPals/signup.html', {'form': form})

class Login(TemplateView):
    template_name = "PunPals/login.html"

class UserHome(ListView):
    template_name = "PunPals/user_home.html"