from rest_framework import viewsets
from .models import Informacao
from .serializers import InformacaoSerializer

class InformacaoViewSet(viewsets.ModelViewSet):
    queryset = Informacao.objects.all()
    serializer_class = InformacaoSerializer
