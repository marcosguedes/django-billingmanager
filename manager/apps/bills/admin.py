from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _, ngettext
from rangefilter.filter import DateRangeFilter

from .forms import BillForm
from .models import Bill, BillSource, RecurrentBill


# Register your models here.
@admin.register(RecurrentBill)
class RecurrentBillAdmin(admin.ModelAdmin):
    list_display = ["__str__", "value", "periodicity", "date_start", "active"]
    list_editable = ["active"]
    filter_horizontal = ["tenants"]
    actions = ["generate_bills"]
    save_as = True

    def generate_bills(self, request, queryset):
        today = timezone.now().date()
        total_bills = []
        error_msgs = []

        for obj in queryset:
            try:
                total_bills.extend(obj.generate_bills())
            except ValidationError as e:
                error_msgs.extend(e)

        if total_bills and error_msgs:
            self.message_user(
                request,
                ngettext(
                    "%(count)d bill was created but there were errors",
                    "%(count)d bills were created but there were errors",
                    len(total_bills),
                )
                % {"count": len(total_bills)},
                level=messages.WARNING,
            )
        elif total_bills:
            self.message_user(
                request,
                ngettext(
                    "%(count)d bill was successfully created",
                    "%(count)d bills were successfully created",
                    len(total_bills),
                )
                % {"count": len(total_bills)},
                level=messages.SUCCESS,
            )
        else:
            self.message_user(request, _("No bills created"), level=messages.WARNING)

        if error_msgs:
            self.message_user(
                request,
                mark_safe(
                    "There were errors generating bills:{}".format(
                        "".join(["<br>{}".format(msg) for msg in error_msgs])
                    )
                ),
                level=messages.ERROR,
            )

    generate_bills.short_description = _("Generate bills up to now")


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    date_hierarchy = "date"
    list_display = ["__str__", "value", "date"]
    list_editable = ["date"]
    filter_horizontal = ["tenants"]
    list_filter = ["tenants", ("date", DateRangeFilter), "source"]
    form = BillForm
    save_as = True


admin.site.register(BillSource, admin.ModelAdmin)
