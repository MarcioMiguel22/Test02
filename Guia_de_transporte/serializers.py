"""
Documento de Serializadores para Guia de Transporte.
Responsável por converter os objetos do modelo GuiaDeTransporte para formatos como JSON,
facilitando a comunicação da API REST.
"""
from rest_framework import serializers
from .models import GuiaDeTransporte

class GuiaDeTransporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuiaDeTransporte
        fields = ['id', 'item', 'descricao', 'unidade', 'quantidade', 'peso', 'volume']
