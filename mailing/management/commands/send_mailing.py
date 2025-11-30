from django.core.management.base import BaseCommand, CommandError

from mailing.models import Mailing
from mailing.services import send_mailing_now


class Command(BaseCommand):
    help = "Отправить рассылку по её ID"

    def add_arguments(self, parser):
        parser.add_argument("mailing_id", type=int, help="ID рассылки")

    def handle(self, *args, **options):
        mailing_id = options["mailing_id"]
        try:
            mailing = Mailing.objects.get(pk=mailing_id)
        except Mailing.DoesNotExist:
            raise CommandError(f"Рассылка с id={mailing_id} не найдена")

        self.stdout.write(f"Запуск рассылки #{mailing.id}...")
        send_mailing_now(mailing)
        self.stdout.write(self.style.SUCCESS("Рассылка завершена."))
