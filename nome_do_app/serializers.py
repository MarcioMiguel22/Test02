from rest_framework import serializers
from .models import CodigoEntrada

class CodigoEntradaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodigoEntrada
        fields = '__all__'
