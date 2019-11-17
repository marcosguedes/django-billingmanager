from django import template
from django.db.models.aggregates import Sum

from bank_account.models import Deposit, Withdrawal
from tenants.models import Tenant


register = template.Library()


@register.inclusion_tag("tenants/tenant_controlpanel.html", takes_context=True)
def tenant_controlpanel(context):
    # request = context.get("request", None)

    context["tenants"] = Tenant.objects.all()
    deposit_total_value = Deposit.objects.all().aggregate(total_value=Sum("value"))
    withdrawal_total_value = Withdrawal.objects.all().aggregate(
        total_value=Sum("value")
    )
    try:
        total_balance = (
            deposit_total_value["total_value"] - withdrawal_total_value["total_value"]
        )
    except TypeError:
        # There were no deposits and/or withdrawals
        deposits = deposit_total_value["total_value"]
        withdrawals = withdrawal_total_value["total_value"]

        total_balance = deposits

        if withdrawals:
            total_balance = -withdrawals

    total_balance = total_balance if total_balance else 0

    context["total_balance"] = total_balance + sum(
        [t.get_balance() for t in Tenant.objects.all()]
    )

    return context
