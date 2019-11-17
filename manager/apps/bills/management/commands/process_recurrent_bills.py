from django.core.management.base import BaseCommand, CommandError
from bills.models import RecurrentBill


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def handle(self, *args, **options):
        try:
            RecurrentBill.process_recurrent_bills()
            self.stdout.write(self.style.SUCCESS("Bill generation process ended"))
        except Exception as e:
            self.stdout.write(
                self.style.ERROR("There were errors generating bills. %s" % e)
            )
