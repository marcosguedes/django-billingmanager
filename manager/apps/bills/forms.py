from django import forms

from .models import Bill


class BillForm(forms.ModelForm):
    date = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = Bill
        fields = ["source", "name", "value", "date", "tenants", "observations"]
