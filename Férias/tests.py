from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Vacation
from datetime import date

class VacationModelTests(TestCase):
    def test_vacation_creation(self):
        """Test that a vacation record can be created"""
        vacation = Vacation.objects.create(
            employee_name="Test Employee",
            start_date=date(2023, 7, 1),
            end_date=date(2023, 7, 15),
            status="pending",
            reason="Testing"
        )
        self.assertEqual(vacation.employee_name, "Test Employee")
        self.assertEqual(vacation.status, "pending")

class VacationAPITests(APITestCase):
    def setUp(self):
        """Create test data"""
        self.vacation = Vacation.objects.create(
            employee_name="API Test",
            start_date=date(2023, 8, 1),
            end_date=date(2023, 8, 10),
            status="pending"
        )
        
    def test_get_vacation_list(self):
        """Test retrieving vacation list"""
        url = reverse('vacation-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        
    def test_create_vacation(self):
        """Test creating a new vacation record"""
        url = reverse('vacation-list')
        data = {
            'employee_name': 'New Employee',
            'start_date': '2023-09-01',
            'end_date': '2023-09-15',
            'reason': 'API Test Creation'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vacation.objects.count(), 2)
        
    def test_get_pending_vacations(self):
        """Test filtering by pending status"""
        url = reverse('vacation-pending')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
