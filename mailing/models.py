from django.conf import settings
from django.db import models


class Recipient(models.Model):
    """Получатель рассылки (клиент)."""

    email = models.EmailField(
        verbose_name="Email",
        unique=True,
    )
    full_name = models.CharField(
        verbose_name="Ф. И. О.",
        max_length=255,
    )
    comment = models.TextField(
        verbose_name="Комментарий",
        blank=True,
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Владелец",
        on_delete=models.CASCADE,
        related_name="recipients",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Получатель рассылки"
        verbose_name_plural = "Получатели рассылок"
        ordering = ["email"]

    def __str__(self) -> str:
        return f"{self.full_name} <{self.email}>"


class Message(models.Model):
    """Сообщение, которое будет отправляться в рассылке."""

    subject = models.CharField(
        verbose_name="Тема письма",
        max_length=255,
    )
    body = models.TextField(
        verbose_name="Тело письма",
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Владелец",
        on_delete=models.CASCADE,
        related_name="messages",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["subject"]

    def __str__(self) -> str:
        return self.subject


class Mailing(models.Model):
    """Рассылка."""

    STATUS_CREATED = "created"
    STATUS_RUNNING = "running"
    STATUS_FINISHED = "finished"

    STATUS_CHOICES = [
        (STATUS_CREATED, "Создана"),
        (STATUS_RUNNING, "Запущена"),
        (STATUS_FINISHED, "Завершена"),
    ]

    start_at = models.DateTimeField(
        verbose_name="Дата и время первой отправки",
    )
    end_at = models.DateTimeField(
        verbose_name="Дата и время окончания отправки",
    )
    status = models.CharField(
        verbose_name="Статус",
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_CREATED,
    )

    message = models.ForeignKey(
        Message,
        verbose_name="Сообщение",
        on_delete=models.CASCADE,
        related_name="mailings",
    )
    recipients = models.ManyToManyField(
        Recipient,
        verbose_name="Получатели",
        related_name="mailings",
        blank=True,
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Владелец",
        on_delete=models.CASCADE,
        related_name="mailings",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["-start_at"]

    def __str__(self) -> str:
        return f"Рассылка #{self.pk} ({self.get_status_display()})"


class MailingAttempt(models.Model):
    """Попытка отправки сообщения по рассылке."""

    STATUS_SUCCESS = "success"
    STATUS_FAILED = "failed"

    STATUS_CHOICES = [
        (STATUS_SUCCESS, "Успешно"),
        (STATUS_FAILED, "Не успешно"),
    ]

    mailing = models.ForeignKey(
        Mailing,
        verbose_name="Рассылка",
        on_delete=models.CASCADE,
        related_name="attempts",
    )
    attempted_at = models.DateTimeField(
        verbose_name="Дата и время попытки",
        auto_now_add=True,
    )
    status = models.CharField(
        verbose_name="Статус",
        max_length=20,
        choices=STATUS_CHOICES,
    )
    server_response = models.TextField(
        verbose_name="Ответ почтового сервера",
        blank=True,
    )

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылок"
        ordering = ["-attempted_at"]

    def __str__(self) -> str:
        return f"Попытка #{self.pk} для рассылки #{self.mailing_id}"
