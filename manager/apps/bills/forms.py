from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Bill


class BillForm(forms.ModelForm):
    date = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = Bill
        fields = ["source", "name", "value", "date", "tenants", "observations"]
        help_texts = {
            "value": _(
                "Value will be divided by the number of selected Tenants upon save"
            )
        }
