from rest_framework import viewsets
from .models import CodigoEntrada
from .serializers import CodigoEntradaSerializer

class CodigoEntradaViewSet(viewsets.ModelViewSet):
    queryset = CodigoEntrada.objects.all()
    serializer_class = CodigoEntradaSerializer
