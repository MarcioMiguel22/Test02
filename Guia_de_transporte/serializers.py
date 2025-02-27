from rest_framework import serializers
from .models import GuiaDeTransporte

class GuiaDeTransporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuiaDeTransporte
        fields = '__all__'
