from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Application
from .forms import RegistrationForm, ApplicationForm
def index(request):
    done_applications = Application.objects.filter(status='done').order_by('-created_at')

    # Пагинация
    paginator = Paginator(done_applications, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'done_applications': page_obj, 
        'is_paginated': page_obj.has_other_pages(), 
        'page_obj': page_obj, 
    }
    return render(request, 'index.html', context)

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


def appliation_views(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save()
            messages.success(request, 'Заявка успешно создана!')
            return redirect('application_success') 
        else:
            messages.error(request, 'Пожалуйста исправте ошибки')
    else:
        form = ApplicationForm()
    return render(request, 'create_application.html', {'form': form})