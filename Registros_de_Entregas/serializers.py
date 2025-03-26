from rest_framework import serializers
from .models import RegistroEntrega

class RegistroEntregaSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroEntrega
        fields = [
            'id', 'obra_id', 'data_entrega', 'numero_instalacao',
            'numero_obra', 'assinatura', 'imagem', 'notas', 'data_criacao',
            'criado_em', 'atualizado_em'
        ]
        read_only_fields = ['id', 'data_criacao', 'criado_em', 'atualizado_em']

    def to_representation(self, instance):
        """Converte para o formato esperado pelo frontend"""
        representation = super().to_representation(instance)
        return {
            'id': str(representation['id']),
            'obraId': representation['obra_id'],
            'dataEntrega': representation['data_entrega'],
            'numeroInstalacao': representation['numero_instalacao'],
            'numeroObra': representation['numero_obra'],
            'assinatura': representation['assinatura'],
            'imagem': representation['imagem'],
            'notas': representation['notas'],
            'dataCriacao': representation['data_criacao'],
        }

    def to_internal_value(self, data):
        """Converte do formato do frontend para o formato interno"""
        # Se os dados vierem no formato do frontend, converter para o formato do modelo
        if 'obraId' in data:
            data = {
                'obra_id': data.get('obraId', ''),
                'data_entrega': data.get('dataEntrega', ''),
                'numero_instalacao': data.get('numeroInstalacao', ''),
                'numero_obra': data.get('numeroObra', ''),
                'assinatura': data.get('assinatura', None),
                'imagem': data.get('imagem', None),
                'notas': data.get('notas', None),
            }
        return super().to_internal_value(data)
