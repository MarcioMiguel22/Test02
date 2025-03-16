"""
Documento de Views para Guia de Transporte.
Responsável por gerenciar as visualizações e endpoints da API para o modelo GuiaDeTransporte.
Utiliza Django REST Framework para criar uma API RESTful.
"""
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.decorators import api_view, parser_classes
from .models import GuiaDeTransporte, TransportItem
from .serializers import GuiaDeTransporteSerializer, TransportItemSerializer
import base64
import os
import logging

# Configure logger
logger = logging.getLogger(__name__)

class GuiaDeTransporteViewSet(viewsets.ModelViewSet):
    queryset = GuiaDeTransporte.objects.all()
    serializer_class = GuiaDeTransporteSerializer
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        try:
            logger.info(f"Update request received for item {instance.id}")
            
            if 'imagem' in request.FILES:
                logger.info(f"Image file received in request.FILES")
                image_file = request.FILES['imagem']
                image_data = base64.b64encode(image_file.read()).decode('utf-8')
                image_type = image_file.content_type
                data = request.data.copy()
                data['imagem'] = f"data:{image_type};base64,{image_data}"
                logger.info(f"Image converted to base64, type: {image_type}")
            else:
                data = request.data
                logger.info("No image file in request")
            
            serializer = self.get_serializer(instance, data=data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            
            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}
            
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error updating item: {str(e)}")
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class GuiaDeTransporteListCreateView(generics.ListCreateAPIView):
    queryset = GuiaDeTransporte.objects.all()
    serializer_class = GuiaDeTransporteSerializer
    parser_classes = (JSONParser, MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        if 'imagem' in request.FILES:
            image_file = request.FILES['imagem']
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
            image_type = image_file.content_type
            data = request.data.copy()
            data['imagem'] = f"data:{image_type};base64,{image_data}"
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return super().create(request, *args, **kwargs)

class TransportItemListCreate(generics.ListCreateAPIView):
    queryset = TransportItem.objects.all()
    serializer_class = TransportItemSerializer
    parser_classes = (JSONParser, MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        if 'imagem' in request.FILES:
            image_file = request.FILES['imagem']
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
            image_type = image_file.content_type
            data = request.data.copy()
            data['imagem'] = f"data:{image_type};base64,{image_data}"
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
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
        
        try:
            logger.info(f"Update request received for TransportItem {instance.id}")
            
            if 'imagem' in request.FILES:
                logger.info("Processing image file in TransportItem update")
                image_file = request.FILES['imagem']
                image_data = base64.b64encode(image_file.read()).decode('utf-8')
                image_type = image_file.content_type
                data = request.data.copy()
                data['imagem'] = f"data:{image_type};base64,{image_data}"
            else:
                data = request.data
            
            serializer = self.get_serializer(instance, data=data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error updating TransportItem: {str(e)}")
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
