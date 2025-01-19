from rest_framework import serializers
from .models import CodigoEntrada

class CodigoEntradaSerializer(serializers.ModelSerializer):
    codigosDaPorta = serializers.ListField(source='get_codigos_da_porta_list', write_only=False)
    Localizacao = serializers.CharField(source='localizacao')
    Instalacao = serializers.CharField(source='instalacao')
    codigoCaves = serializers.CharField(source='codigo_caves')

    class Meta:
        model = CodigoEntrada
        fields = ['id', 'Localizacao', 'Instalacao', 'codigosDaPorta', 'codigoCaves']

    def to_internal_value(self, data):
        # Convert frontend field names to model field names
        internal_data = {
            'localizacao': data.get('Localizacao'),
            'instalacao': data.get('Instalacao'),
            'codigo_caves': data.get('codigoCaves'),
        }
        
        # Handle codigos_da_porta separately
        codigos = data.get('codigosDaPorta', [])
        if isinstance(codigos, list):
            internal_data['codigos_da_porta'] = ', '.join(codigos)
        else:
            internal_data['codigos_da_porta'] = codigos

        return super().to_internal_value(internal_data)
