from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import CustomerUser

def home(request):
    """Главная страница"""
    return render(request, 'catalog/home.html')

def login_view(request):
    """Страница входа"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Вы успешно вошли в систему!")
            return redirect('home')  # Перенаправляем на главную
        else:
            messages.error(request, "Неверный логин или пароль.")
    
    return render(request, 'registration/login.html')

def register(request):
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        full_name = request.POST.get('full_name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Пароли не совпадают.")
        elif CustomerUser.objects.filter(username=username).exists():
            messages.error(request, "Пользователь с таким логином уже существует.")
        elif CustomerUser.objects.filter(email=email).exists():
            messages.error(request, "Пользователь с таким email уже существует.")
        else:
            user = CustomerUser.objects.create_user(
                username=username,
                email=email,
                password=password1,
                full_name=full_name
            )
            user.save()
            login(request, user)
            messages.success(request, "Регистрация прошла успешно! Вы вошли в систему.")
            return redirect('home')

    return render(request, 'registration/register.html')

def logout_view(request):
    """Выход из системы"""
    logout(request)
    messages.info(request, "Вы вышли из системы.")
    return redirect('home')