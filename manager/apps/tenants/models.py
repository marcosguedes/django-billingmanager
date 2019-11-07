from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Tenant(models.Model):
    name = models.CharField(_("Name"), max_length=100)

    class Meta:
        verbose_name = _("Tenant")
        verbose_name_plural = _("Tenants")
        ordering = ("name",)

    def __str__(self):
        return self.name
