from django.contrib import admin

# from django.utils.translation import gettext_lazy as _
from rangefilter.filter import DateRangeFilter
from .models import Deposit, Withdrawal


@admin.register(Deposit)
@admin.register(Withdrawal)
class TransferAdmin(admin.ModelAdmin):
    date_hierarchy = "created"
    list_display = ["__str__", "created"]
    list_filter = ["created"]
    list_filter = [("created", DateRangeFilter)]
