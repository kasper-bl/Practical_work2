from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import re
from .models import Application, CustomerUser

class RegistrationForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=255,
        label='ФИО'
    )
    email = forms.EmailField(
        label='email',
        widget=forms.EmailInput(attrs={ 'placeholder': 'qwe@example.com'})
    )
    agree_personal_data = forms.BooleanField(
        required=True,
        label='Согласие на обработку персональных данных',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
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

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['title', 'description', 'category', 'img_Application']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите описание'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
        