from django.test import TestCase
from rest_framework.test import APIClient, APIRequestFactory, force_authenticate
from .models import RegistroEntrega
from django.contrib.auth.models import User
import uuid
from .views import RegistroEntregaViewSet
import json
from datetime import date, timedelta

class RegistroEntregaAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create test users
        self.admin_user = User.objects.create_superuser(
            username='admin', 
            email='admin@example.com', 
            password='admin123'
        )
        self.regular_user = User.objects.create_user(
            username='user', 
            email='user@example.com', 
            password='user123'
        )
        self.another_user = User.objects.create_user(
            username='another', 
            email='another@example.com', 
            password='another123'
        )
        
        # Create test registros
        self.admin_registro = RegistroEntrega.objects.create(
            obra_id="123",
            data_entrega="2023-10-01",
            numero_instalacao="INS001",
            numero_obra="OBR001",
            assinatura="test-signature",
            imagem="test-image",
            criado_por=self.admin_user
        )
        
        self.user_registro = RegistroEntrega.objects.create(
            obra_id="456",
            data_entrega="2023-10-02",
            numero_instalacao="INS002",
            numero_obra="OBR002",
            assinatura="test-signature-2",
            imagem="test-image-2",
            criado_por=self.regular_user
        )
        
        # Create test registro with images
        image_list = ["image1-base64", "image2-base64"]
        self.registro_with_images = RegistroEntrega.objects.create(
            obra_id="789",
            data_entrega="2023-10-03",
            numero_instalacao="INS003",
            numero_obra="OBR003",
            assinatura="test-signature-3",
            imagem="test-image-3",
            criado_por=self.regular_user
        )
        self.registro_with_images.set_imagens(image_list)
        self.registro_with_images.save()
        
        # Setup request factory for testing views directly
        self.factory = APIRequestFactory()

    def test_listar_registros(self):
        response = self.client.get('/registros/')
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.data), 0)
        
    def test_permissao_edicao(self):
        # Admin can edit any registro
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.patch(
            f'/registros/{self.user_registro.id}/',
            {'notas': 'Updated by admin'}
        )
        self.assertEqual(response.status_code, 200)
        
        # User can edit their own registro
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.patch(
            f'/registros/{self.user_registro.id}/',
            {'notas': 'Updated by owner'}
        )
        self.assertEqual(response.status_code, 200)
        
        # User cannot edit registro created by another user
        self.client.force_authenticate(user=self.another_user)
        response = self.client.patch(
            f'/registros/{self.user_registro.id}/',
            {'notas': 'Should not update'}
        )
        self.assertEqual(response.status_code, 403)
        
    def test_filtro_avancado(self):
        # Test date range filtering
        today = date.today()
        yesterday = today - timedelta(days=1)
        tomorrow = today + timedelta(days=1)
        
        # Create registro with today's date
        RegistroEntrega.objects.create(
            obra_id="999",
            data_entrega=today,
            numero_instalacao="INS999",
            numero_obra="OBR999"
        )
        
        # Test filtering by date range
        response = self.client.get(
            f'/registros/?data_inicio={yesterday}&data_fim={tomorrow}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data['results']), 1)
        
        # Test filtering by creator
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(f'/registros/?criado_por={self.regular_user.id}')
        self.assertEqual(response.status_code, 200)
        # Check that all results are created by regular_user
        for item in response.data['results']:
            self.assertEqual(item['criadoPor']['id'], self.regular_user.id)
            
    def test_images_endpoint(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(f'/registros/{self.registro_with_images.id}/images/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['imagem'], 'test-image-3')
        self.assertEqual(len(response.data['imagens']), 2)
