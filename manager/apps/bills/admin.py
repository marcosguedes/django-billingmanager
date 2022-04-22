from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _, ngettext

from .forms import BillForm
from .models import Bill, BillSource, RecurrentBill, TenantValueBill


@admin.register(RecurrentBill)
class RecurrentBillAdmin(admin.ModelAdmin):
    list_display = ["__str__", "value", "periodicity", "date_start", "active"]
    list_editable = ["active"]
    filter_horizontal = ["tenants"]
    actions = ["generate_bills"]
    save_as = True

    # def generate_bills(self, request, queryset):
    #     total_bills = []
    #     error_msgs = []

    #     for obj in queryset:
    #         try:
    #             total_bills.extend(obj.generate_bills())
    #         except ValidationError as e:
    #             error_msgs.extend(e)

    #     if total_bills and error_msgs:
    #         self.message_user(
    #             request,
    #             ngettext(
    #                 "%(count)d bill was created but there were errors",
    #                 "%(count)d bills were created but there were errors",
    #                 len(total_bills),
    #             )
    #             % {"count": len(total_bills)},
    #             level=messages.WARNING,
    #         )
    #     elif total_bills:
    #         self.message_user(
    #             request,
    #             ngettext(
    #                 "%(count)d bill was successfully created",
    #                 "%(count)d bills were successfully created",
    #                 len(total_bills),
    #             )
    #             % {"count": len(total_bills)},
    #             level=messages.SUCCESS,
    #         )
    #     else:
    #         self.message_user(request, _("No bills created"), level=messages.WARNING)

    #     if error_msgs:
    #         self.message_user(
    #             request,
    #             mark_safe(
    #                 "There were errors generating bills:{}".format(
    #                     "".join(["<br>{}".format(msg) for msg in error_msgs])
    #                 )
    #             ),
    #             level=messages.ERROR,
    #         )

    # generate_bills.short_description = _("Generate bills up to now")


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    date_hierarchy = "date"
    list_display = ["__str__", "value", "date", "paid"]
    list_editable = ["date", "value", "paid"]
    filter_horizontal = ["tenants"]
    list_filter = ["tenants", "date", "paid", "source"]
    actions = ["regenerate_tenant_bill"]
    form = BillForm
    save_as = True

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.instance.split_value_between_tenants()

    def regenerate_tenant_bill(self, request, queryset):

        for obj in queryset:
            TenantValueBill.objects.filter(bill=obj).delete()
            obj.split_value_between_tenants()

        self.message_user(
            request,
            _("Tenant Bills successfully (re)generated"),
            level=messages.SUCCESS,
        )

    regenerate_tenant_bill.short_description = _("(Re)Generate Tenant bills")


admin.site.register(BillSource, admin.ModelAdmin)


@admin.register(TenantValueBill)
class TenantValueBillAdmin(admin.ModelAdmin):
    date_hierarchy = "bill__date"
    list_display = ["__str__", "value", "bill_date"]
    list_filter = ["tenant", "bill__date", "bill__date"]

    def bill_date(self, obj):
        return obj.bill.date.strftime("%d/%m/%Y")

    bill_date.short_description = _("Date")
    bill_date.admin_order_field = "bill__date"
