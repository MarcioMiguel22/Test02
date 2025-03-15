"""
Documento de Serializadores para Guia de Transporte.
Responsável por converter os objetos do modelo GuiaDeTransporte para formatos como JSON,
facilitando a comunicação da API REST.
"""
from rest_framework import serializers
from .models import GuiaDeTransporte, TransportItem

class GuiaDeTransporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuiaDeTransporte
        fields = ['id', 'item', 'descricao', 'em_falta', 'quantidade', 'notas', 'total', 'created_at', 'updated_at']

class TransportItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportItem
        fields = '__all__'
