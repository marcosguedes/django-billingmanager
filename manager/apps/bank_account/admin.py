from django.contrib import admin

# from django.utils.translation import gettext_lazy as _
from .models import Deposit, Withdrawal


@admin.register(Deposit)
@admin.register(Withdrawal)
class TransferAdmin(admin.ModelAdmin):
    date_hierarchy = "created"
    list_display = ["__str__", "created", "tenant"]
    list_filter = ["created", "tenant"]
