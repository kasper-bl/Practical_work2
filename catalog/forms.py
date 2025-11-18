from django import forms
from django.core.exceptions import ValidationError
import re
from django.contrib.auth import get_user_model
from .models import Application, CustomerUser

class RegistrationForm(forms.ModelForm):
    full_name = forms.CharField(
        max_length=255,
        label='ФИО',
        widget=forms.TextInput(attrs = {'class': 'form-control'}) 
    )
    email = forms.EmailField(
        label='email',
        widget=forms.EmailInput(attrs={ 'class': 'form-control', 'placeholder': 'qwe@example.com'})
    )
    agree_personal_data = forms.BooleanField(
        required=True,
        label='Согласие на обработку персональных данных',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.match(r'^[a-zA-Z\-]+$', username):
            raise ValidationError('Логин должен содержать только латинские буквы и дефис')
        return username
        
    def clean_full_name(self):
        full_name = self.cleaned_data['full_name']
        if not re.match(r'^[а-яёА-ЯЁ\s\-]+$', full_name):
            raise ValidationError('ФИО должно состоять только из кириллицы, пробелов и дефиса')
        return full_name
    
    def clean_agree_personal_data(self):
        agree = self.cleaned_data['agree_personal_data']
    
    class Meta:
        model = CustomerUser
        fields = ['username', 'email', 'full_name', 'agree_personal_data']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин'}),
        }
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('Пароли не совпадают')
        return password2

    def save(self, commit=True): 
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['title', 'description', 'category', 'img_Application']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите описание'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
        
    def clean_img_Application(self):
        img = self.cleaned_data.get('img_Application')
        if img:
            if img.size > 2 * 1024 * 1024: 
                raise ValidationError('Размер файла не должен превышать 2 МБ.')
        return img