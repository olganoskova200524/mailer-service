from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, TemplateView

from .forms import UserRegisterForm, UserLoginForm

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

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        self.send_activation_email(user)

        messages.success(
            self.request,
            "Вы успешно зарегистрировались. "
            "Проверьте почту и подтвердите email по ссылке в письме.",
        )
        return redirect("login")

    def send_activation_email(self, user: User) -> None:
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        activation_link = self.request.build_absolute_uri(
            reverse("users:activate", kwargs={"uidb64": uid, "token": token})
        )

        subject = "Подтверждение регистрации"
        message = render_to_string(
            "registration/activation_email.txt",
            {
                "user": user,
                "activation_link": activation_link,
            },
        )

        user.email_user(subject, message)


class ProfileView(LoginRequiredMixin, TemplateView):
    """Страница профиля (если нужна)"""
    template_name = "users/profile.html"


class ActivateEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Email подтверждён. Теперь вы можете войти.")
            return redirect("login")

        return render(request, "registration/activation_invalid.html")
