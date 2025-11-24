from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Кастомная модель пользователя:
    - авторизация по email
    - дополнительные поля: аватар, телефон, страна
    """

    username = None
    email = models.EmailField(
        verbose_name="Email",
        unique=True,
    )

    avatar = models.ImageField(
        verbose_name="Аватар",
        upload_to="users/avatars/",
        blank=True,
        null=True,
        help_text='Загрузите свой аватар',
    )
    phone = models.CharField(
        verbose_name="Номер телефона",
        max_length=20,
        blank=True,
        help_text='Введите номер телефона',
    )
    country = models.CharField(
        verbose_name="Страна",
        max_length=100,
        blank=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
