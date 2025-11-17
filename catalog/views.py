from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import CustomerUser
from .forms import RegistrationForm

def home(request):
    return render(request, 'catalog/index.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Вы успешно вошли в систему!")
            return redirect('index')
        else:
            messages.error(request, "Неверный логин или пароль.")
    
    return render(request, 'registration/login.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Сохраняем пользователя
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация прошла успешно! Вы вошли в систему.")
            return redirect('index')
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "Вы вышли из системы.")
    return redirect('index')

def home(request):
    return render(request, 'index.html')