from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from ..models import Avaria, Material  # type: ignore
from ..avarias_a_receber.serializers import AvariaSerializer, MaterialSerializer



class AvariaListCreate(generics.ListCreateAPIView):
    queryset = Avaria.objects.all()
    serializer_class = AvariaSerializer

class AvariaRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Avaria.objects.all()
    serializer_class = AvariaSerializer

class MaterialListCreate(generics.ListCreateAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

class MaterialRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
