"""
Documento de Configuração de URLs para Guia de Transporte.
Define os padrões de URL da aplicação e mapeia as requisições aos respectivos views.
Utiliza o sistema de roteamento do Django REST Framework para criar endpoints da API.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GuiaDeTransporteViewSet

router = DefaultRouter()
router.register(r'guias', GuiaDeTransporteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
