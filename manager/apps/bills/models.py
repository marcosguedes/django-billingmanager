from django.db import models
from django.db.models.deletion import SET_NULL
from django.template.defaultfilters import date
from django.utils import timezone
from django.utils.translation import gettext_lazy as _, gettext_noop, gettext
from django_extensions.db.models import TimeStampedModel

from tenants.models import Tenant


class BillSource(models.Model):
    """
    :summary: Source of a bill. Can be a
    company name (i.e. EDP) or the name
    of the utility (i.e. Electricity)
    """

    name = models.CharField(verbose_name=_("Name"), max_length=100)

    class Meta:
        verbose_name = _("Bill Source")
        verbose_name_plural = _("Bill Sources")
        ordering = ("name",)

    def __str__(self):
        return self.name

    def get_related_bills(self):
        return self.bills_bill_related.all()


class AbstractBill(models.Model):
    source = models.ForeignKey(
        BillSource,
        verbose_name=_("Bill Source"),
        null=True,
        on_delete=SET_NULL,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=100,
        blank=True,
        help_text=_("Optional. Source can be used instead of name"),
    )
    value = models.DecimalField(
        verbose_name=_("Value"),
        max_digits=9,
        decimal_places=2,
        # TODO: Place this help_text in Bill's ModelForm only
        help_text=_(
            "Value will be divided by the number of selected Tenants upon save"
        ),
    )
    observations = models.TextField(verbose_name=_("Observations"), blank=True)
    tenants = models.ManyToManyField(
        Tenant,
        verbose_name=_("Tenants"),
        help_text=_("The bill's total value is divided by the number of tenants"),
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name if self.name else str(self.source)


class RecurrentBill(AbstractBill):
    """
    :summary: Model that periodically creates bills
    according to a date and period. If its Start Date
    is set to 8 of November with a monthly period,
    each bill will be created at the 8th day of
    every month
    """

    PERIODICITY_MONTHLY = "monthly"
    PERIODICITY_YEARLY = "yearly"
    PERIODICITY_CHOICES = (
        (PERIODICITY_MONTHLY, gettext_noop(PERIODICITY_MONTHLY)),
        (PERIODICITY_YEARLY, gettext_noop(PERIODICITY_YEARLY)),
    )
    date_start = models.DateField(
        verbose_name=_("Start Date"),
        help_text=_(
            "Bills will be created starting from this \
            date and with a period set by Periodicity"
        ),
    )
    periodicity = models.CharField(
        verbose_name=_("Periodicity"),
        max_length=100,
        choices=PERIODICITY_CHOICES,
        default=PERIODICITY_MONTHLY,
        help_text=_(
            "Ignore the day. Bills are generated in the first of every a month / year"
        ),
    )
    active = models.BooleanField(verbose_name=_("Active"), default=False)

    class Meta:
        verbose_name = _("Recurrent Bill")
        verbose_name_plural = _("Recurrent Bills")
        ordering = ("active", "date_start")

    def get_related_bills(self):
        return self.source.get_related_bills()

    def can_generate_bill(self, date=None):
        """
        Retrieve any bill issued in the current year or month if the Recurrent
        Bill isn't set in the future. If no bill was found, then we can generate
        a bill
        """
        if not date:
            date = timezone.now()
        if self.date_start > date:
            return False

        bills_generated_on_date_year = self.get_related_bills().filter(
            date__year=date.year
        )
        bills_generated_on_date_month = bills_generated_on_date_year.filter(
            date__month=date.month
        )
        return (
            not bills_generated_on_date_month.exists()
            if self.periodicity == self.PERIODICITY_MONTHLY
            else not bills_generated_on_date_year.exists()
        )

    def generate_bills(self):
        pass


class Bill(AbstractBill, TimeStampedModel):
    """
    :summary: The bill itself. Will create several TenantValueBill on save
    depending on the number of tenants with its value split between them
    """

    date = models.DateField(verbose_name=_("Date"))  # use SelectDateWidget

    class Meta:
        verbose_name = _("Bill")
        verbose_name_plural = _("Bills")


class TenantValueBill(TimeStampedModel):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    value = models.DecimalField(
        verbose_name=_("Value"),
        max_digits=9,
        decimal_places=2,
        help_text=_(
            "Value will be divided by the number of selected Tenants upon save"
        ),
    )
    paid = models.BooleanField(verbose_name=_("Paid"), default=False)

    class Meta:
        verbose_name = _("Tenant Bill")
        verbose_name_plural = _("Tenant Bills")

    def __str__(self):
        return "%(name)s: %(bill)s (%(status)s)" % {
            "bill": self.bill,
            "name": self.name,
            "date": date(self.bill.date, "F Y"),
            "status": gettext("Paid") if self.paid else gettext("Unpaid"),
        }
