from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from django.utils import timezone
from django.db.models import Count, Q
from django.contrib.auth import get_user_model

from .models import Mailing, Recipient, Message, MailingAttempt


def send_mailing_now(mailing: Mailing) -> None:
    """
    Отправляет письма по рассылке всем её получателям
    и создаёт записи MailingAttempt для каждой попытки.
    """

    if mailing.status == Mailing.STATUS_CREATED:
        mailing.status = Mailing.STATUS_RUNNING
        mailing.save(update_fields=["status"])

    subject = mailing.message.subject
    body = mailing.message.body
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None)

    for recipient in mailing.recipients.all():
        try:
            sent_count = send_mail(
                subject,
                body,
                from_email,
                [recipient.email],
                fail_silently=False,
            )
            if sent_count > 0:
                MailingAttempt.objects.create(
                    mailing=mailing,
                    attempted_at=timezone.now(),
                    status=MailingAttempt.STATUS_SUCCESS,
                    server_response="Отправлено успешно",
                )
            else:
                MailingAttempt.objects.create(
                    mailing=mailing,
                    attempted_at=timezone.now(),
                    status=MailingAttempt.STATUS_FAILED,
                    server_response="send_mail вернул 0 (письмо не отправлено)",
                )
        except Exception as exc:
            MailingAttempt.objects.create(
                mailing=mailing,
                attempted_at=timezone.now(),
                status=MailingAttempt.STATUS_FAILED,
                server_response=str(exc),
            )

    if mailing.end_at <= timezone.now():
        mailing.status = Mailing.STATUS_FINISHED
        mailing.save(update_fields=["status"])


def get_user_stats(user):
    """
    Статистика по конкретному пользователю.
    Результат кешируется на 60 секунд.
    """
    cache_key = f"user_stats_{user.pk}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    mailings_qs = Mailing.objects.filter(owner=user)
    recipients_qs = Recipient.objects.filter(owner=user)
    messages_qs = Message.objects.filter(owner=user)
    attempts_qs = MailingAttempt.objects.filter(mailing__owner=user)

    attempts_agg = attempts_qs.aggregate(
        total=Count("id"),
        success=Count("id", filter=Q(status=MailingAttempt.STATUS_SUCCESS)),
        failed=Count("id", filter=Q(status=MailingAttempt.STATUS_FAILED)),
    )

    total = attempts_agg["total"] or 0
    success = attempts_agg["success"] or 0
    failed = attempts_agg["failed"] or 0
    success_rate = round(success / total * 100, 1) if total > 0 else 0

    mailings_stats = mailings_qs.annotate(
        attempts_total=Count("attempts"),
        attempts_success=Count(
            "attempts",
            filter=Q(attempts__status=MailingAttempt.STATUS_SUCCESS),
        ),
        attempts_failed=Count(
            "attempts",
            filter=Q(attempts__status=MailingAttempt.STATUS_FAILED),
        ),
    )

    data = {
        "mailings_count": mailings_qs.count(),
        "recipients_count": recipients_qs.count(),
        "messages_count": messages_qs.count(),
        "attempts_total": total,
        "attempts_success": success,
        "attempts_failed": failed,
        "attempts_success_rate": success_rate,
        "mailings_stats": mailings_stats,
    }

    cache.set(cache_key, data, timeout=60)
    return data


def get_global_stats():
    """
    Общесистемная статистика (для менеджера).
    Результат кешируется на 60 секунд.
    """
    cache_key = "global_stats"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    mailings_qs = Mailing.objects.all()
    recipients_qs = Recipient.objects.all()
    messages_qs = Message.objects.all()
    attempts_qs = MailingAttempt.objects.all()

    attempts_agg = attempts_qs.aggregate(
        total=Count("id"),
        success=Count("id", filter=Q(status=MailingAttempt.STATUS_SUCCESS)),
        failed=Count("id", filter=Q(status=MailingAttempt.STATUS_FAILED)),
    )

    total = attempts_agg["total"] or 0
    success = attempts_agg["success"] or 0
    failed = attempts_agg["failed"] or 0
    success_rate = round(success / total * 100, 1) if total > 0 else 0

    mailings_stats = mailings_qs.annotate(
        attempts_total=Count("attempts"),
        attempts_success=Count(
            "attempts",
            filter=Q(attempts__status=MailingAttempt.STATUS_SUCCESS),
        ),
        attempts_failed=Count(
            "attempts",
            filter=Q(attempts__status=MailingAttempt.STATUS_FAILED),
        ),
    )

    User = get_user_model()
    users_stats = User.objects.annotate(
        mailings_count=Count("mailings", distinct=True),
        attempts_total=Count("mailings__attempts"),
        attempts_success=Count(
            "mailings__attempts",
            filter=Q(mailings__attempts__status=MailingAttempt.STATUS_SUCCESS),
        ),
        attempts_failed=Count(
            "mailings__attempts",
            filter=Q(mailings__attempts__status=MailingAttempt.STATUS_FAILED),
        ),
    )

    data = {
        "mailings_count": mailings_qs.count(),
        "recipients_count": recipients_qs.count(),
        "messages_count": messages_qs.count(),
        "attempts_total": total,
        "attempts_success": success,
        "attempts_failed": failed,
        "attempts_success_rate": success_rate,
        "mailings_stats": mailings_stats,
        "users_stats": users_stats,
    }

    cache.set(cache_key, data, timeout=60)
    return data
