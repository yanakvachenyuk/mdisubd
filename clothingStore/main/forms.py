from django import forms
from django.db import connection

class LoginForm(forms.Form):
    email = forms.CharField(max_length=100, label='Почта')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')

