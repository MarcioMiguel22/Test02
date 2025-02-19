from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Avaria, Material  # Corrected import
from .serializers import AvariaSerializer, MaterialSerializer  # Corrected import

class AvariaListCreate(generics.ListCreateAPIView):
    queryset = Avaria.objects.all()
    serializer_class = AvariaSerializer

    def create(self, request, *args, **kwargs):
        print("Received data:", request.data)  # Add logging
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class AvariaRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Avaria.objects.all()
    serializer_class = AvariaSerializer

class MaterialListCreate(generics.ListCreateAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

class MaterialRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
