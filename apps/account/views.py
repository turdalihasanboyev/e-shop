from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password)
        login(request, user)
        return redirect('home')

    return render(request, 'register.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('login')

    return render(request, 'login.html')

def home_view(request):
    return render(request, 'index.html')
