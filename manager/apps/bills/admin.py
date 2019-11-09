from datetime import datetime

from dateutil import rrule
from django.contrib import admin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .forms import BillForm
from .models import Bill, BillSource, RecurrentBill


# Register your models here.
@admin.register(RecurrentBill)
class RecurrentBillAdmin(admin.ModelAdmin):
    list_display = ["__str__", "value", "periodicity", "active"]
    list_editable = ["active"]
    filter_horizontal = ["tenants"]
    actions = ["generate_bills"]
    save_as = True

    def generate_bills(self, request, queryset):
        today = timezone.now().date()
        month_first_day = datetime.date(today.year, today.month, 1)
        for obj in queryset:
            if obj.periodicity == RecurrentBill.PERIODICITY_MONTHLY:
                dates = [
                    dt
                    for dt in rrule(
                        rrule.MONTHLY, dtstart=obj.date_start, until=month_first_day
                    )
                ]

        queryset.update(status="p")

    generate_bills.short_description = _("Generate bills up to now")


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ["__str__", "value", "date"]
    list_editable = ["date"]
    filter_horizontal = ["tenants"]
    form = BillForm
    save_as = True


admin.site.register(BillSource, admin.ModelAdmin)
