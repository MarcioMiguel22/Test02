from rest_framework import serializers
from .models import CodigoEntrada

class CodigoEntradaSerializer(serializers.ModelSerializer):
    codigosDaPorta = serializers.ListField(
        source='get_codigos_da_porta_list',
        write_only=False,
        required=False,
        allow_empty=True,
        default=list
    )
    Localizacao = serializers.CharField(source='localizacao', allow_blank=True, required=True)
    Instalacao = serializers.CharField(source='instalacao', allow_blank=True, required=True)
    codigoCaves = serializers.CharField(source='codigo_caves', allow_blank=True, required=True)

    class Meta:
        model = CodigoEntrada
        fields = ['id', 'Localizacao', 'Instalacao', 'codigosDaPorta', 'codigoCaves']

    def to_internal_value(self, data):
        if not isinstance(data, dict):
            return super().to_internal_value(data)
            
        internal_data = {
            'localizacao': data.get('Localizacao', ''),
            'instalacao': data.get('Instalacao', ''),
            'codigo_caves': data.get('codigoCaves', ''),
        }
        
        codigos = data.get('codigosDaPorta', [])
        if isinstance(codigos, list):
            internal_data['codigos_da_porta'] = ', '.join(str(code) for code in codigos)
        else:
            internal_data['codigos_da_porta'] = str(codigos)

        return internal_data

    def validate(self, attrs):
        # Ensure required fields are present
        required_fields = ['localizacao', 'instalacao', 'codigo_caves']
        for field in required_fields:
            if not attrs.get(field):
                raise serializers.ValidationError({field: 'This field is required.'})
        return attrs
