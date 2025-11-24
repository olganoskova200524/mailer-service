from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import UserRegisterForm

User = get_user_model()


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "users/profile.html"
