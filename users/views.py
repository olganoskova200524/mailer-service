from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView   # ← добавили
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import UserRegisterForm, UserLoginForm  # ← добавили UserLoginForm

User = get_user_model()


class UserLoginView(LoginView):
    """Вход по email"""
    form_class = UserLoginForm
    template_name = "registration/login.html"


class RegisterView(CreateView):
    """Регистрация пользователя"""
    model = User
    form_class = UserRegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")


class ProfileView(LoginRequiredMixin, TemplateView):
    """Страница профиля (если нужна)"""
    template_name = "users/profile.html"
