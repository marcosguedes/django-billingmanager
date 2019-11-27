from dateutil.relativedelta import relativedelta
from django.db.models.aggregates import Sum
from django.test import TestCase
from django.utils import timezone

from bills.models import BillSource, RecurrentBill, Bill, TenantValueBill
from tenants.models import Tenant


# Create your tests here.
class BillTests(TestCase):
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

    def split_value_between_tenants(self):
        # Should generate three bills and split them
        # between 3 tenants
        RecurrentBill.process_recurrent_bills()

        for bill in Bill.objects.all():
            bill.split_value_between_tenants()

    def test_recurrent_bill_generation(self):
        """
        Should automatically generate two recurrent Bills, plus
        one single
        """
        RecurrentBill.process_recurrent_bills()
        self.assertEqual(Bill.objects.filter(source=self.recurrent_source).count(), 2)
        self.assertEqual(Bill.objects.all().count(), 3)

    def test_tenantvaluebill_number(self):
        """
        Should generate 3 tenant bills for each bill, with the
        total of 9 (3x3)
        """
        self.split_value_between_tenants()

        self.assertEqual(TenantValueBill.objects.all().count(), 9)

    def test_total_values(self):
        self.split_value_between_tenants()
        total_bill_values = Bill.objects.all().aggregate(Sum("value"))["value__sum"]

        for tenant in Tenant.objects.all():
            total_tenant_bill_value = tenant.get_bills().aggregate(Sum("value"))[
                "value__sum"
            ]
            self.assertAlmostEqual(
                total_tenant_bill_value,
                total_bill_values / Tenant.objects.all().count(),
                places=1,
            )
