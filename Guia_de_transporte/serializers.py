"""
Documento de Serializadores para Guia de Transporte.
Responsável por converter os objetos do modelo GuiaDeTransporte para formatos como JSON,
facilitando a comunicação da API REST.
"""
from rest_framework import serializers
from .models import GuiaDeTransporte, TransportItem
import logging

logger = logging.getLogger(__name__)

class GuiaDeTransporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuiaDeTransporte
        fields = ['id', 'item', 'descricao', 'unidade', 'quantidade', 'peso', 'volume', 
                 'notas', 'em_falta', 'total', 'imagem', 'created_at', 'updated_at']
    
    def validate(self, data):
        # Log the validation process for debugging
        logger.info(f"Validating GuiaDeTransporte data: {list(data.keys())}")
        if 'imagem' in data:
            logger.info(f"Image data present, length: {len(str(data['imagem']))}")
        return data

class TransportItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportItem
        fields = '__all__'
    
    def validate(self, data):
        # Log the validation process for debugging
        logger.info(f"Validating TransportItem data: {list(data.keys())}")
        if 'imagem' in data:
            logger.info(f"Image data present, length: {len(str(data['imagem']))}")
        return data
