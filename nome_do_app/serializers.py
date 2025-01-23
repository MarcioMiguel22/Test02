from rest_framework import serializers
from .models import CodigoEntrada

class CodigoEntradaSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Corrigir valores inválidos
        data['codigos_da_porta'] = (
            [] if data['codigos_da_porta'] in [None, 'nan'] else data['codigos_da_porta'].split(',')
        )
        return data

    class Meta:
        model = CodigoEntrada
        model = CodigoEntrada
        fields = '__all__'
