from rest_framework import viewsets
from .models import GuiaDeTransporte
from .serializers import GuiaDeTransporteSerializer

class GuiaDeTransporteViewSet(viewsets.ModelViewSet):
    queryset = GuiaDeTransporte.objects.all()
    serializer_class = GuiaDeTransporteSerializer
