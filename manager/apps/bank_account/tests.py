from dateutil.relativedelta import relativedelta
from django.db.models.aggregates import Sum
from django.test import TestCase
from django.utils import timezone

from bills.models import BillSource, RecurrentBill, Bill, TenantValueBill
from tenants.models import Tenant


# Create your tests here.
class AccountAndBalanceTests(TestCase):
    def setUp(self):
        # month_first_day = datetime.date(timezone.now().year, timezone.now().month, 1)
        self.today = timezone.now().date()
        last_month = self.today - relativedelta(months=1)
        self.tenant_1 = Tenant.objects.create(name="Tenant 1")
        self.tenant_2 = Tenant.objects.create(name="Tenant 2")
        self.tenant_3 = Tenant.objects.create(name="Tenant 3")
        self.recurrent_source = BillSource.objects.create(name="Test Recurrent Source")
        self.single_source = BillSource.objects.create(name="Test Single Source")
        self.recurrent_bill = RecurrentBill.objects.create(
            date_start=last_month,
            periodicity=RecurrentBill.PERIODICITY_MONTHLY,
            active=True,
            source=self.recurrent_source,
            value=10,
        )

        self.bill = Bill.objects.create(source=self.single_source, value=10)

        for tenant in Tenant.objects.all():
            self.recurrent_bill.tenants.add(tenant)
            self.bill.tenants.add(tenant)

    def test_simple(self):
        self.assertEqual(1 + 1, 2)
