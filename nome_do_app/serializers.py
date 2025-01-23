from rest_framework import serializers
from .models import CodigoEntrada

class CodigoEntradaSerializer(serializers.ModelSerializer):
    codigos_da_porta = serializers.ListField(
        child=serializers.CharField(max_length=255),
        allow_empty=True
    )

    class Meta:
        model = CodigoEntrada
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Assegura que codigos_da_porta é uma lista
        if isinstance(data['codigos_da_porta'], str):
            data['codigos_da_porta'] = (
                [] if data['codigos_da_porta'].lower() == 'nan' else data['codigos_da_porta'].split(',')
            )
        return data

    def to_internal_value(self, data):
        # Converte a lista de volta para string ao salvar
        if 'codigos_da_porta' in data and isinstance(data['codigos_da_porta'], list):
            data['codigos_da_porta'] = ','.join(data['codigos_da_porta'])
        return super().to_internal_value(data)
