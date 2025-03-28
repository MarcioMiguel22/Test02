from rest_framework import serializers
from .models import DespesaCarro
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

class DespesaCarroSerializer(serializers.ModelSerializer):
    criadoPor = UserSerializer(source='usuario', read_only=True)
    
    class Meta:
        model = DespesaCarro
        fields = [
            'id', 'tipo_combustivel', 'valor_despesa', 'data_despesa', 
            'quilometragem', 'imagem', 'imagens', 'observacoes', 
            'data_criacao', 'usuario_criacao', 'criadoPor'
        ]
        read_only_fields = ['id', 'data_criacao', 'usuario_criacao']
        
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['usuario'] = user
        validated_data['usuario_criacao'] = user.username
        return super().create(validated_data)
