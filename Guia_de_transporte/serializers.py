from rest_framework import serializers
from .models import Informacao

class InformacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Informacao
        fields = '__all__'
