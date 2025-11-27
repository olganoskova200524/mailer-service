from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Введите email",
        })
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Введите пароль",
        })
    )


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "avatar", "phone", "country",)

        widgets = {
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Введите email",
            }),
            "avatar": forms.ClearableFileInput(attrs={
                "class": "form-control",
            }),
            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Введите номер телефона",
            }),
            "country": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Введите страну",
            }),
        }

    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Введите пароль",
        })
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Повторите пароль",
        })
    )
