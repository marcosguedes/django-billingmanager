from django.db import models
from django.utils.translation import gettext_lazy as _, gettext
from django_extensions.db.models import TimeStampedModel

# Create your models here.


class BaseTransfer(TimeStampedModel):

    value = models.DecimalField(verbose_name=_("Value"), max_digits=9, decimal_places=2)

    class Meta:
        abstract = True


class Deposit(BaseTransfer):
    class Meta:
        verbose_name = _("Deposit")
        verbose_name_plural = _("Deposits")
        ordering = ("-created",)

    def __str__(self):
        return gettext("Deposited %d€") % self.value


class Withdrawal(BaseTransfer):
    class Meta:
        verbose_name = _("Withdrawal")
        verbose_name_plural = _("Withdrawals")
        ordering = ("-created",)

    def __str__(self):
        return gettext("Withdrawed %d€") % self.value
