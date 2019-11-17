from django.apps import AppConfig


class BillsConfig(AppConfig):
    name = "bills"

    def ready(self):
        # Check if there are bills to generate
        # each time the project starts
        from bills.models import RecurrentBill

        RecurrentBill.process_recurrent_bills()
