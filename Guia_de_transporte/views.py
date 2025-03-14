"""
Documento de Views para Guia de Transporte.
Responsável por gerenciar as visualizações e endpoints da API para o modelo GuiaDeTransporte.
Utiliza Django REST Framework para criar uma API RESTful.
"""
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from .models import GuiaDeTransporte, TransportItem
from .serializers import GuiaDeTransporteSerializer, TransportItemSerializer

class GuiaDeTransporteViewSet(viewsets.ModelViewSet):
    queryset = GuiaDeTransporte.objects.all()
    serializer_class = GuiaDeTransporteSerializer

class GuiaDeTransporteListCreateView(generics.ListCreateAPIView):
    queryset = GuiaDeTransporte.objects.all()
    serializer_class = GuiaDeTransporteSerializer

class TransportItemListCreate(generics.ListCreateAPIView):
    queryset = TransportItem.objects.all()
    serializer_class = TransportItemSerializer
    parser_classes = (JSONParser, MultiPartParser, FormParser)  # Added parsers for form data

    def create(self, request, *args, **kwargs):
        # Handle both JSON and form data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class TransportItemRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = TransportItem.objects.all()
    serializer_class = TransportItemSerializer
    parser_classes = (JSONParser, MultiPartParser, FormParser)  # Added parsers for form data

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
