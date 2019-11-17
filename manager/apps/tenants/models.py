from django.db import models
from django.db.models.aggregates import Sum
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Tenant(models.Model):
    name = models.CharField(_("Name"), max_length=100)

    class Meta:
        verbose_name = _("Tenant")
        verbose_name_plural = _("Tenants")
        ordering = ("name",)

    def __str__(self):
        return self.name

    def get_bills(self):
        return self.tenantvaluebill_set.all()

    def get_transfer_totals(self):
        deposits = self.bank_account_deposit_related.all().aggregate(
            total_value=Sum("value")
        )
        withdrawals = self.bank_account_withdrawal_related.all().aggregate(
            total_value=Sum("value")
        )
        deposit_total_value = deposits["total_value"]
        withdrawal_total_value = withdrawals["total_value"]

        try:
            bank_totals = deposit_total_value - withdrawal_total_value
        except TypeError:
            # There were no deposits and/or withdrawals
            bank_totals = deposit_total_value

            if withdrawal_total_value:
                bank_totals = -withdrawal_total_value

        return bank_totals if bank_totals else 0

    def get_balance(self):
        total_bill_values = self.get_bills().aggregate(total_value=Sum("value"))

        if total_bill_values["total_value"]:
            return self.get_transfer_totals() - total_bill_values["total_value"]
        return self.get_transfer_totals()
