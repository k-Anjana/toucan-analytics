from django.test import TestCase
from analytics.models import CustomerData, EMIData
from datetime import date

class CustomerDataTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        CustomerData.objects.create(
            customer_Id=1,
            category='Regular',
            mode_of_payments='Credit Card',
            amount_spent=100.0,
            date='2023-05-31'
        )


    def test_model_creation(self):
        obj = CustomerData.objects.get(customer_Id=1)
        self.assertEqual(obj.customer_Id, 1)
        self.assertEqual(obj.category, 'Regular')
        self.assertEqual(obj.mode_of_payments, 'Credit Card')
        self.assertEqual(obj.amount_spent, 100.0)
        self.assertEqual(obj.date, date(2023, 5, 31))


    def test_model_update(self):
        obj = CustomerData.objects.get(customer_Id=1)
        obj.amount_spent = 150.0
        obj.save()

        updated_obj = CustomerData.objects.get(pk=obj.pk)
        self.assertEqual(updated_obj.amount_spent, 150.0)

    def test_model_deletion(self):
        obj = CustomerData.objects.get(customer_Id=1)
        obj.delete()

        self.assertFalse(CustomerData.objects.filter(customer_Id=1).exists())


class EMIDataTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        EMIData.objects.create(customer_Id=1, EMI_paid_on_time='True')

    def test_model_creation(self):
        obj = EMIData.objects.get(customer_Id=1)
        self.assertEqual(obj.customer_Id, 1)
        self.assertEqual(obj.EMI_paid_on_time, 'True')

    def test_model_update(self):
        obj = EMIData.objects.get(customer_Id=1)
        obj.EMI_paid_on_time = 'False'
        obj.save()

        updated_obj = EMIData.objects.get(pk=obj.pk)
        self.assertEqual(updated_obj.EMI_paid_on_time, 'False')

    def test_model_deletion(self):
        obj = EMIData.objects.get(customer_Id=1)
        obj.delete()

        self.assertFalse(EMIData.objects.filter(customer_Id=1).exists())

from django.test import TestCase
from django.http import JsonResponse
from .models import CustomerData, EMIData
from .views import table, bar, pie, emi


class AnalyticsTestCase(TestCase):
    def setUp(self):
        # Create test data
        CustomerData.objects.create(
            customer_Id=1,
            category='Regular',
            mode_of_payments='Credit Card',
            amount_spent=100.0,
            date='2023-05-31'
        )
        EMIData.objects.create(
            customer_Id=1,
            EMI_paid_on_time='Yes'
        )

    def test_table_view(self):
        response = table(None, '2023-05-01', '2023-05-31')
        self.assertIsInstance(response, JsonResponse)
        # Add assertions for the response data if required

    def test_bar_view(self):
        response = bar(None, '2023-05-01', '2023-05-31')
        self.assertIsInstance(response, JsonResponse)
        # Add assertions for the response data if required

    def test_pie_view(self):
        response = pie(None, '2023-05-01', '2023-05-31')
        self.assertIsInstance(response, JsonResponse)
        # Add assertions for the response data if required

    def test_emi_view(self):
        response = emi(None)
        self.assertIsInstance(response, JsonResponse)
        # Add assertions for the response data if required
