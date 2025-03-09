from django.test import TestCase
from rest_framework.test import APIClient
from .models import RegistroEntrega
import uuid

class RegistroEntregaAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_registro = RegistroEntrega.objects.create(
            obra_id="123",
            data_entrega="2023-10-01",
            numero_instalacao="INS001",
            numero_obra="OBR001",
            assinatura="test-signature",
            imagem="test-image"
        )

    def test_listar_registros(self):
        response = self.client.get('/registros/')
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.data), 0)
