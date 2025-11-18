from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Application
from .forms import RegistrationForm, ApplicationForm
from django.contrib.auth.decorators import login_required, user_passes_test


def index(request):
    done_applications = Application.objects.filter(status='done').order_by('-created_at')
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
    return redirect('index')

@login_required
def user_application(request):
    status_filter = request.GET.get('status', '')
    applications = Application.objects.filter(user=request.user)
    if status_filter:
        applications = applications.filter(status = status_filter)

    paginator = Paginator(applications, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'applications': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,
        'status_filter': status_filter,
    }
    return render(request, 'user_application.html', context)


@login_required
def application_views(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            messages.success(request, 'Заявка успешно создана!')
            return redirect('index') 
        else:
            messages.error(request, 'Пожалуйста исправте ошибки')
    else:
        form = ApplicationForm()
    return render(request, 'create_application.html', {'form': form})

@login_required
def delete_application(request, pk):
    application = get_object_or_404(Application, pk=pk)
    if request.method == 'POST':
        application.delete()
        messages.success(request, 'Удалено')
        return redirect('user_application')
    context = {
        'application': application
    }
    return render(request, 'delete_application_confirm.html', context)


def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def admin_applications(request):
    """Страница для админа - список всех заявок"""
    status_filter = request.GET.get('status', '')
    
    applications = Application.objects.all()
    if status_filter:
        applications = applications.filter(status=status_filter)
    
    context = {
        'applications': applications,
        'status_filter': status_filter,
    }
    return render(request, 'admin_applications.html', context)

@login_required
@user_passes_test(is_superuser)
def change_status(request, pk):
    """Изменение статуса заявки админом"""
    application = get_object_or_404(Application, pk=pk)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        
        # Проверка правил смены статуса
        if application.status == 'new':
            if new_status == 'done':
                # Для статуса "Выполнено" нужно изображение
                if 'design_image' in request.FILES:
                    application.img_Application = request.FILES['design_image']
                    application.status = new_status
                    application.save()
                    messages.success(request, 'Статус заявки изменён на "Выполнено"')
                else:
                    messages.error(request, 'Для статуса "Выполнено" нужно прикрепить изображение')
                    return redirect('admin_applications')
                    
            elif new_status == 'accepted':
                # Для статуса "Принято в работу" нужно указать комментарий
                comment = request.POST.get('comment', '').strip()
                if comment:
                    application.comment = comment
                    application.status = new_status
                    application.save()
                    messages.success(request, 'Статус заявки изменён на "Принято в работу"')
                else:
                    messages.error(request, 'Для статуса "Принято в работу" нужно указать комментарий')
                    return redirect('admin_applications')
            else:
                messages.error(request, 'Недопустимый статус')
                return redirect('admin_applications')
                
        else:
            messages.error(request, 'Нельзя изменить статус заявки, которая не в статусе "Новая"')
            return redirect('admin_applications')
        
        return redirect('admin_applications')
    
    return redirect('admin_applications')