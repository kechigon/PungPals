import hashlib
from django.views.generic import TemplateView, ListView
from django.shortcuts import render, redirect

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

#class Login(TemplateView):
#    template_name = "PunPals/login.html"

class UserHome(TemplateView):
    template_name = "PunPals/user_home.html"