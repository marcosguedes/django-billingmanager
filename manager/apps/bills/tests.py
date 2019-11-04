from django.test import TestCase

# Create your tests here.


class BillTests(TestCase):
    def setUp(self):
        pass

    def simple_test(self):
        self.assertEqual(1 + 1, 2)
