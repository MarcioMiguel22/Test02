from rest_framework import serializers
from .models import RegistroEntrega
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

class RegistroEntregaSerializer(serializers.ModelSerializer):
    # Explicitly define imagens as a field since it's a property in the model
    imagens = serializers.ListField(child=serializers.CharField(), required=False, allow_empty=True, allow_null=True)
    criado_por = UserSerializer(read_only=True)
    
    class Meta:
        model = RegistroEntrega
        fields = [
            'id', 'obra_id', 'data_entrega', 'data_entrega_doc', 'data_trabalho_finalizado',
            'numero_instalacao', 'numero_obra', 'assinatura', 'imagem', 'imagens', 'notas', 
            'data_criacao', 'criado_em', 'atualizado_em', 'criado_por'
        ]
        read_only_fields = ['id', 'data_criacao', 'criado_em', 'atualizado_em', 'criado_por']

    def to_representation(self, instance):
        """Converte para o formato esperado pelo frontend"""
        representation = super().to_representation(instance)
        
        # Get images from the model's field using the helper method
        if hasattr(instance, 'get_imagens'):
            representation['imagens'] = instance.get_imagens()
        
        # Get creator information
        criado_por = representation.get('criado_por')
        
        return {
            'id': str(representation['id']),
            'obraId': representation['obra_id'],
            'dataEntrega': representation['data_entrega'],
            'dataEntregaDoc': representation['data_entrega_doc'],
            'dataTrabalhoFinalizado': representation['data_trabalho_finalizado'],
            'numeroInstalacao': representation['numero_instalacao'],
            'numeroObra': representation['numero_obra'],
            'assinatura': representation['assinatura'],
            'imagem': representation['imagem'],
            'imagens': representation['imagens'],
            'notas': representation['notas'],
            'dataCriacao': representation['data_criacao'],
            'criadoPor': criado_por,
        }

    def to_internal_value(self, data):
        """Converte do formato do frontend para o formato interno"""
        internal_data = {}
        
        # Se os dados vierem no formato do frontend, converter para o formato do modelo
        if 'obraId' in data:
            internal_data['obra_id'] = data.get('obraId', '')
            internal_data['data_entrega'] = data.get('dataEntrega', '')
            internal_data['data_entrega_doc'] = data.get('dataEntregaDoc', None)
            internal_data['data_trabalho_finalizado'] = data.get('dataTrabalhoFinalizado', None)
            internal_data['numero_instalacao'] = data.get('numeroInstalacao', '')
            internal_data['numero_obra'] = data.get('numeroObra', '')
            internal_data['assinatura'] = data.get('assinatura', None)
            internal_data['imagem'] = data.get('imagem', None)
            internal_data['notas'] = data.get('notas', None)
            
            # Handle images list separately to prevent losing it during conversion
            if 'imagens' in data:
                # This will be handled by the custom create/update methods
                internal_data['imagens'] = data.get('imagens', [])
            
            return internal_data
        
        # If data isn't in frontend format, process normally
        return super().to_internal_value(data)
        
    def create(self, validated_data):
        imagens = validated_data.pop('imagens', []) if 'imagens' in validated_data else []
        instance = super().create(validated_data)
        
        # Set images separately using the helper method
        if imagens:
            instance.set_imagens(imagens)
            instance.save()
            
        return instance
        
    def update(self, instance, validated_data):
        # Get images before removing from validated_data
        imagens = validated_data.pop('imagens', None)
        
        # Update other fields
        instance = super().update(instance, validated_data)
        
        # Update images separately if included in the request
        if imagens is not None:
            instance.set_imagens(imagens)
            instance.save()
            
        return instance
