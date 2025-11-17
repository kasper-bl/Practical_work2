from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import re
from .models import CustomerUser

class RegistrationForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=255,
        label='ФИО',
        widget=forms.TextInput(attrs={'class': 'form=control'})
    )
    email = forms.EmailField(
        label='email',
        widget=forms.EmailInput(attrs={'class': 'form=control', 'placeholder': 'qwe@example.com'})
    )
    agree_personal_data = forms.BooleanField(
        required=True,
        label='Согласие на обработку персональных данных',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = CustomerUser
        fields = ['username', 'email', 'full_name', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={ 'placeholder': 'Только латиница и дефис'})
        }
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.match(r'^[a-zA-Z\-]+', username):
            raise ValidationError('Логин должен содержать только латинские буквы и дефис')
        
    def clean_full_name(self):
        full_name = self.cleaned_data['full_name']
        if not re.match(r'^[а-яёА-ЯЁ]\s\-]+', full_name):
            raise ValidationError('ФИО должно состоять только из кириллицы, пробелов и дефиса')
    def clean_agree_personal_data(self):
        agree = self.cleaned_data['agree_personal_data']