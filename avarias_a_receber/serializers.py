from rest_framework import serializers
from .models import Avaria, Material

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
