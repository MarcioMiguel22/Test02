from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import CodigoEntrada

# Create your tests here.

class HomeViewTests(TestCase):
    def test_home_view_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

class CodigoEntradaAPITests(APITestCase):
    def setUp(self):
        # Criar um objeto para testar
        self.codigo = CodigoEntrada.objects.create(
            localizacao="Teste Localização",
            instalacao="Teste Instalação",
            codigos_da_porta="123,456",
            codigo_caves="789"
        )
        self.detail_url = reverse('nome_do_app:codigoentrada-detail', args=[self.codigo.id])
    
    def test_delete_codigo_entrada(self):
        """
        Testa se a operação DELETE está funcionando corretamente.
        """
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CodigoEntrada.objects.count(), 0)
