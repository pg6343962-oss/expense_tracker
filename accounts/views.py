from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth. decorators import login_required
from .forms import RegisterForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})

from django.contrib.auth.views import LoginView
from django.contrib.auth import logout

class CustomLoginView(LoginView):
    template_name = "accounts/login.html"

def logout_view(request):
    logout(request)
    return redirect("home")

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

class CustomPasswordChangeView(PasswordChangeView):
    template_name = "accounts/change_password.html"
    success_url = reverse_lazy("profile")