from django.test import TestCase
from django.urls import reverse

# Create your tests here.

class HomeViewTests(TestCase):
    def test_home_view_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

class LocalDeChavesTests(TestCase):
    def test_local_de_chaves_status_code(self):
        response = self.client.get(reverse('local-de-chaves'))
        self.assertEqual(response.status_code, 200)

class AdministracaoTests(TestCase):
    def test_administracao_status_code(self):
        response = self.client.get(reverse('administracao'))
        self.assertEqual(response.status_code, 200)
