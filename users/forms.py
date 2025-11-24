from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2", "avatar", "phone", "country")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["email"].label = "Email"
        self.fields["password1"].label = "Пароль"
        self.fields["password2"].label = "Подтверждение пароля"
