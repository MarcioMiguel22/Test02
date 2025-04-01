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
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from datetime import datetime

logger = logging.getLogger(__name__)

class RegistroEntregaViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite operações CRUD em Registros de Entrega
    """
    queryset = RegistroEntrega.objects.all()
    serializer_class = RegistroEntregaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'numero_obra', 'numero_instalacao', 
        'data_entrega', 'data_entrega_doc', 'data_trabalho_finalizado',
        'data_criacao', 'tipo_documento'
    ]
    search_fields = ['numero_obra', 'numero_instalacao', 'notas']
    ordering_fields = [
        'data_entrega', 'data_entrega_doc', 'data_trabalho_finalizado',
        'data_criacao', 'criado_em', 'tipo_documento'
    ]
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        """
        Lista registros de entrega com otimização para carregamento mais rápido
        quando o número de registros for grande.
        """
        try:
            # Apply filters, search, and ordering
            queryset = self.filter_queryset(self.get_queryset())
            
            # Apply additional advanced filtering if needed
            queryset = self._apply_advanced_filters(request, queryset)
            
            # Optimize query by limiting loaded data per page
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error in list method: {str(e)}")
            return Response(
                {"error": "Erro ao listar registros", "detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def _apply_advanced_filters(self, request, queryset):
        """
        Aplica filtros avançados baseados nos parâmetros de query.
        Suporta filtragem por período de data e outros filtros complexos.
        """
        # Get query parameters
        params = request.query_params
        
        # Filter by date ranges if provided
        for date_field in ['data_entrega', 'data_entrega_doc', 'data_trabalho_finalizado']:
            inicio_param = f'{date_field}_inicio'
            fim_param = f'{date_field}_fim'
            
            inicio = params.get(inicio_param)
            fim = params.get(fim_param)
            
            if inicio and fim:
                try:
                    # Convert to datetime objects
                    inicio_dt = datetime.strptime(inicio, '%Y-%m-%d')
                    fim_dt = datetime.strptime(fim, '%Y-%m-%d')
                    
                    # Create filter parameter dynamically
                    date_range_filter = {f'{date_field}__range': (inicio_dt, fim_dt)}
                    queryset = queryset.filter(**date_range_filter)
                except ValueError:
                    # In case of invalid date format, just log and continue
                    logger.warning(f"Invalid date format for {date_field}: {inicio} - {fim}")
        
        # Filter by tipo_documento if provided
        tipo_documento = params.get('tipo_documento')
        if tipo_documento:
            queryset = queryset.filter(tipo_documento=tipo_documento)
        
        # Filter by criado_por if requested
        criado_por = params.get('criado_por')
        if criado_por:
            queryset = queryset.filter(criado_por__id=criado_por)
            
        return queryset

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            # Save with the authenticated user as creator
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            logger.error(f"Error creating registro: {str(e)}")
            return Response(
                {"error": "Erro ao criar registro", "detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def perform_create(self, serializer):
        # Only set the creator if the user is authenticated
        if self.request.user.is_authenticated:
            serializer.save(criado_por=self.request.user)
        else:
            serializer.save()

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            
            # Check if user has permission to update
            if not self._has_update_permission(request.user, instance):
                return Response(
                    {"error": "Você não tem permissão para editar este registro"},
                    status=status.HTTP_403_FORBIDDEN
                )
                
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            
            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}
                
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error updating registro: {str(e)}")
            return Response(
                {"error": "Erro ao atualizar registro", "detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def partial_update(self, request, *args, **kwargs):
        """
        Método explícito para lidar com atualizações parciais (PATCH).
        Reutiliza a lógica do método update com partial=True.
        """
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            
            # Check if user has permission to delete
            if not self._has_update_permission(request.user, instance):
                return Response(
                    {"error": "Você não tem permissão para remover este registro"},
                    status=status.HTTP_403_FORBIDDEN
                )
                
            self.perform_destroy(instance)
            return Response(
                {"success": "Registro removido com sucesso"},
                status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            logger.error(f"Error deleting registro: {str(e)}")
            return Response(
                {"error": "Erro ao remover registro", "detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def _has_update_permission(self, user, instance):
        """
        Verifica se o usuário tem permissão para atualizar ou excluir um registro.
        Só o criador do registro ou um admin pode modificá-lo.
        """
        # Allow if user is admin
        if user.is_staff or user.is_superuser:
            return True
            
        # Allow if user is the creator
        if instance.criado_por and instance.criado_por == user:
            return True
            
        # Deny otherwise
        return False

    @action(detail=True, methods=['get'])
    def images(self, request, pk=None):
        """
        Endpoint para retornar apenas as imagens de um registro
        para carregamento mais rápido em interfaces específicas.
        """
        try:
            registro = self.get_object()
            
            # Return only images data
            return Response({
                'id': str(registro.id),
                'imagem': registro.imagem,
                'imagens': registro.get_imagens()
            })
        except Exception as e:
            logger.error(f"Error fetching images: {str(e)}")
            return Response(
                {"error": "Erro ao buscar imagens", "detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'])
    def document_types(self, request):
        """
        Endpoint para retornar os tipos de documento disponíveis
        """
        try:
            # Get the choices from the model
            choices = dict(RegistroEntrega.TIPO_DOCUMENTO_CHOICES)
            
            # Return formatted choices
            return Response({
                'success': True,
                'document_types': [
                    {'value': key, 'label': label} for key, label in choices.items()
                ]
            })
        except Exception as e:
            logger.error(f"Error fetching document types: {str(e)}")
            return Response(
                {"error": "Erro ao buscar tipos de documento", "detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

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
                'data_entrega': registro.data_entrega,
                'data_entrega_doc': registro.data_entrega_doc,
                'data_trabalho_finalizado': registro.data_trabalho_finalizado,
                'tipo_documento': registro.tipo_documento,
                'tipo_documento_display': dict(RegistroEntrega.TIPO_DOCUMENTO_CHOICES).get(registro.tipo_documento, 'Desconhecido'),
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
