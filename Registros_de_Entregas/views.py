from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework import status
from .models import RegistroEntrega
from .serializers import RegistroEntregaSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import default_storage
import base64
import uuid
from django.http import JsonResponse
import json
import logging
import traceback

class RegistroEntregaViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite operações CRUD em Registros de Entrega
    """
    queryset = RegistroEntrega.objects.all()
    serializer_class = RegistroEntregaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['numero_obra', 'numero_instalacao', 'data_entrega', 'data_criacao']
    search_fields = ['numero_obra', 'numero_instalacao', 'notas']
    ordering_fields = ['data_entrega', 'data_criacao', 'criado_em']
    pagination_class = PageNumberPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Save with the authenticated user as creator
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        # Set the creator to the current authenticated user
        serializer.save(criado_por=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class RegistroDiagnosticView(APIView):
    """
    Diagnostic view for troubleshooting registro data issues
    """
    def get(self, request, pk=None):
        try:
            registro = RegistroEntrega.objects.get(pk=pk)
            
            # Get raw data from the database
            raw_data = {
                'id': str(registro.id),
                'imagens_raw': registro.imagens,  # Raw JSON string from DB
                'imagens_parsed': registro.get_imagens(),  # Parsed list
                'imagem': registro.imagem,
                'model_fields': {field.name: field.get_internal_type() for field in RegistroEntrega._meta.fields}
            }
            
            # Return detailed diagnostic info
            return Response({
                'success': True,
                'diagnostic_info': raw_data,
                'serialized_data': RegistroEntregaSerializer(registro).data
            }, status=status.HTTP_200_OK)
            
        except RegistroEntrega.DoesNotExist:
            return Response(
                {"error": f"Registro with ID {pk} not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            # Return detailed error info
            return Response({
                'success': False,
                'error': str(e),
                'traceback': traceback.format_exc()
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RegistroUploadImagesView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request, pk=None):
        try:
            registro = RegistroEntrega.objects.get(pk=pk)
            
            # Get the initial state
            initial_images = registro.get_imagens()
            
            # Collect all image files from the request
            image_files = []
            
            # Look for fields named imagem_0, imagem_1, etc.
            i = 0
            while f'imagem_{i}' in request.FILES:
                image_files.append(request.FILES[f'imagem_{i}'])
                i += 1
            
            if not image_files:
                return Response(
                    {"error": "No image files found in the request"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Save each image file and convert to base64
            saved_images = []
            for img_file in image_files:
                # Generate a unique name for the image
                img_name = f"{registro.pk}_{uuid.uuid4()}_{img_file.name}"
                
                # Save the image file to storage
                file_path = default_storage.save(f'registros/images/{img_name}', img_file)
                
                # Read file and convert to base64 for storage
                with default_storage.open(file_path) as f:
                    image_data = f.read()
                    base64_image = base64.b64encode(image_data).decode('utf-8')
                    saved_images.append(base64_image)
                
                # Clean up the file since we're storing it as base64
                default_storage.delete(file_path)
            
            # Update the registro with the new images
            current_images = registro.get_imagens() or []
            current_images.extend(saved_images)
            
            registro.set_imagens(current_images)
            registro.save()
            
            # Verify images were saved correctly
            final_images = registro.get_imagens()
            
            # Return the updated registro
            serializer = RegistroEntregaSerializer(registro)
            return Response({
                'success': True,
                'data': serializer.data,
                'debug_info': {
                    'initial_image_count': len(initial_images) if initial_images else 0,
                    'added_image_count': len(saved_images),
                    'final_image_count': len(final_images) if final_images else 0
                }
            }, status=status.HTTP_200_OK)
            
        except RegistroEntrega.DoesNotExist:
            return Response(
                {"error": f"Registro with ID {pk} not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            # Return detailed error info for debugging
            return Response({
                'success': False,
                'error': str(e),
                'traceback': traceback.format_exc()
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
