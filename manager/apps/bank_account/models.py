from django.db import models
from django.utils.translation import gettext_lazy as _, gettext
from django_extensions.db.models import TimeStampedModel
from tenants.models import Tenant

# Create your models here.


class BaseTransfer(TimeStampedModel):
    tenant = models.ForeignKey(
        Tenant,
        verbose_name=_("Tenant"),
        null=True,
        on_delete=models.SET_NULL,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )

    notes = models.TextField(verbose_name=_("Notes"), blank=True)
    value = models.DecimalField(verbose_name=_("Value"), max_digits=9, decimal_places=2)

    class Meta:
        abstract = True


class Deposit(BaseTransfer):
    class Meta:
        verbose_name = _("Deposit")
        verbose_name_plural = _("Deposits")
        ordering = ("-created",)

    def __str__(self):
        return gettext("%s deposited %d€") % (
            self.tenant if self.tenant else _("Empty"),
            self.value,
        )


class Withdrawal(BaseTransfer):
    class Meta:
        verbose_name = _("Withdrawal")
        verbose_name_plural = _("Withdrawals")
        ordering = ("-created",)

    def __str__(self):
        return gettext("%s withdrawed %d€") % (
            self.tenant if self.tenant else _("Empty"),
            self.value,
        )
