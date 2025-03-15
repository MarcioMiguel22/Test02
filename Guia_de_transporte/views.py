"""
Documento de Views para Guia de Transporte.
Responsável por gerenciar as visualizações e endpoints da API para o modelo GuiaDeTransporte.
Utiliza Django REST Framework para criar uma API RESTful.
"""
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.decorators import api_view, parser_classes
from .models import GuiaDeTransporte, TransportItem
from .serializers import GuiaDeTransporteSerializer, TransportItemSerializer
import base64
import os

class GuiaDeTransporteViewSet(viewsets.ModelViewSet):
    queryset = GuiaDeTransporte.objects.all()
    serializer_class = GuiaDeTransporteSerializer
    parser_classes = (JSONParser, MultiPartParser, FormParser)

class GuiaDeTransporteListCreateView(generics.ListCreateAPIView):
    queryset = GuiaDeTransporte.objects.all()
    serializer_class = GuiaDeTransporteSerializer
    parser_classes = (JSONParser, MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        # Processar imagem se enviada como arquivo
        if 'imagem' in request.FILES:
            image_file = request.FILES['imagem']
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
            image_type = image_file.content_type
            request.data._mutable = True
            request.data['imagem'] = f"data:{image_type};base64,{image_data}"
            request.data._mutable = False
        
        return super().create(request, *args, **kwargs)

class TransportItemListCreate(generics.ListCreateAPIView):
    queryset = TransportItem.objects.all()
    serializer_class = TransportItemSerializer
    parser_classes = (JSONParser, MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        # Processar imagem se enviada como arquivo
        if 'imagem' in request.FILES:
            image_file = request.FILES['imagem']
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
            image_type = image_file.content_type
            request.data._mutable = True
            request.data['imagem'] = f"data:{image_type};base64,{image_data}"
            request.data._mutable = False
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class TransportItemRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = TransportItem.objects.all()
    serializer_class = TransportItemSerializer
    parser_classes = (JSONParser, MultiPartParser, FormParser)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        # Processar imagem se enviada como arquivo
        if 'imagem' in request.FILES:
            image_file = request.FILES['imagem']
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
            image_type = image_file.content_type
            request.data._mutable = True
            request.data['imagem'] = f"data:{image_type};base64,{image_data}"
            request.data._mutable = False
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
