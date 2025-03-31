from rest_framework import serializers
from .models import Avaria, Material, RatesConfiguration

class AvariaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avaria
        fields = '__all__'
        
    def validate(self, data):
        # Ensure current_user is provided when creating new avarias
        request = self.context.get('request')
        if request and request.method == 'POST' and 'current_user' not in data:
            raise serializers.ValidationError("current_user field is required")
        return data

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'

class RatesConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatesConfiguration
        fields = ['id', 'standard_rate', 'stop_rate', 'after_11pm_surcharge', 'current_user']
