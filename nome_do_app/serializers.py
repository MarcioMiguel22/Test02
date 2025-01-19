# Importamos o módulo serializers do Django Rest Framework, que nos permite
# criar classes para transformar (serializar) objetos do banco de dados
# em formatos como JSON, bem como validar dados de entrada.
from rest_framework import serializers

# Importamos o modelo CodigoEntrada, que queremos serializar.
from .models import CodigoEntrada

# Definimos uma classe CodigoEntradaSerializer que herda de ModelSerializer.
# Um ModelSerializer facilita a criação de um serializer baseado diretamente
# em um modelo do Django.
class CodigoEntradaSerializer(serializers.ModelSerializer):
    # A classe Meta define qual modelo será serializado e quais campos
    # serão incluídos na serialização.
    class Meta:
        model = CodigoEntrada  # Especifica o modelo a ser usado
        fields = '__all__'     # Inclui todos os campos do modelo
