from django.shortcuts import render, redirect

from django.contrib.auth import get_user_model

from django.contrib import messages

from django.contrib.auth import logout, login, authenticate

from django.contrib.auth.decorators import login_required

User = get_user_model()


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Foydalanuvchi tizimdan muvaffaqiyatli chiqdi!")
    return redirect('home')

def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Parollar bir xil emas!")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username allaqachon mavjud!")
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.save()
        messages.success(request, "Foydalanuchi muvaffaqiyatli ro'yhatdan o'tdi")
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
            messages.success(request, "Foydalanuvchi muvaffaqiyatli tizimga kirdi!")
            return redirect('home')
        else:
            messages.error(request, "Parol yoki username xato!")
            return redirect('login')

    return render(request, 'login.html')

def home_view(request):
    return render(request, 'index.html')
