from rest_framework import serializers
from .models import Avaria


class AvariaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avaria
        fields = '__all__'
