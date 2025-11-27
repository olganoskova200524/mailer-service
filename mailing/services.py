from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from .models import Mailing, MailingAttempt


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
