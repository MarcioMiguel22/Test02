from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from ..models import Avaria  # type: ignore
from ..avarias_a_receber.serializers import AvariaSerializer



class AvariaListCreate(generics.ListCreateAPIView):
    queryset = Avaria.objects.all()
    serializer_class = AvariaSerializer

class AvariaRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Avaria.objects.all()
    serializer_class = AvariaSerializer
