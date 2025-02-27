"""
Documento de Views para Guia de Transporte.
Responsável por gerenciar as visualizações e endpoints da API para o modelo GuiaDeTransporte.
Utiliza Django REST Framework para criar uma API RESTful.
"""
from rest_framework import viewsets
from .models import GuiaDeTransporte
from .serializers import GuiaDeTransporteSerializer

class GuiaDeTransporteViewSet(viewsets.ModelViewSet):
    queryset = GuiaDeTransporte.objects.all()
    serializer_class = GuiaDeTransporteSerializer
