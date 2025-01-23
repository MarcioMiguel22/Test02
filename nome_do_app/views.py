import logging
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from django.db import IntegrityError
from rest_framework.decorators import action
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from .models import CodigoEntrada
from .serializers import CodigoEntradaSerializer

# Configuração do logger
logger = logging.getLogger(__name__)


def home(request):
    """
    Renderiza a página inicial (home.html).
    """
    return render(request, 'home.html')


class CodigoEntradaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para o modelo CodigoEntrada. Provê operações de CRUD completas:
    list, retrieve, create, update, partial_update e destroy.
    """
    queryset = CodigoEntrada.objects.all()
    serializer_class = CodigoEntradaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'localizacao',
        'instalacao',
        'codigos_da_porta',
        'codigo_caves',
        'local_de_chaves',
        'tipo_de_contrato',
        'administracao',
    ]

    def list(self, request, *args, **kwargs):
        """
        Lista todas as instâncias de CodigoEntrada com suporte a filtros e paginação.
        """
        try:
            queryset = self.filter_queryset(self.get_queryset())

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Erro no CodigoEntradaViewSet.list: {str(e)}")
            return Response(
                {"error": "Erro interno no servidor."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def create(self, request, *args, **kwargs):
        """
        Lida com criação de registros:
          - Se receber uma lista, cria cada item individualmente.
          - Se receber um objeto único, cria normalmente.
        """
        data = request.data

        # Verifica se os dados são uma lista para criação em massa
        if isinstance(data, list):
            serializer = self.get_serializer(data=data, many=True)
            try:
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            except IntegrityError as e:
                logger.error(f"IntegrityError durante criação em massa: {str(e)}")
                return Response(
                    {"error": "Erro de integridade durante a criação em massa."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except Exception as e:
                logger.error(f"Erro durante criação em massa: {str(e)}")
                return Response(
                    {"error": "Erro interno durante a criação em massa."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        # Se for objeto único, segue comportamento normal do DRF
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['post'], url_path='sync')
    def sync(self, request):
        """
        Limpa todos os registros e insere novos dados.
        Apenas usuários administradores podem executar esta ação.
        """
        try:
            # Verifica se o usuário tem permissão para executar a ação
            if not request.user.is_staff:
                return Response({"error": "Permissão negada."}, status=status.HTTP_403_FORBIDDEN)

            # Deleta todos os registros existentes
            CodigoEntrada.objects.all().delete()

            # Cria novos registros a partir dos dados enviados
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            logger.error(f"IntegrityError durante a sincronização: {str(e)}")
            return Response(
                {"error": "Erro de integridade durante a sincronização."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Erro durante a sincronização: {str(e)}")
            return Response(
                {"error": "Erro interno durante a sincronização."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CodigoListCreateAPIView(generics.ListCreateAPIView):
    """
    API para listar e criar instâncias de CodigoEntrada com suporte a filtros.
    """
    queryset = CodigoEntrada.objects.all()
    serializer_class = CodigoEntradaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'localizacao',
        'instalacao',
        'codigos_da_porta',
        'codigo_caves',
        'local_de_chaves',
        'tipo_de_contrato',
        'administracao',
    ]

    def get(self, request, *args, **kwargs):
        """
        Lida com requisições GET para listar todas as instâncias de CodigoEntrada.
        """
        try:
            queryset = self.filter_queryset(self.get_queryset())

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Erro no CodigoListCreateAPIView.get: {str(e)}")
            return Response(
                {"error": "Erro interno no servidor."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request, *args, **kwargs):
        """
        Lida com requisições POST para criar novas instâncias de CodigoEntrada.
        """
        data = request.data

        # Verifica se os dados são uma lista para criação em massa
        if isinstance(data, list):
            serializer = self.get_serializer(data=data, many=True)
            try:
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            except IntegrityError as e:
                logger.error(f"IntegrityError durante criação em massa no CodigoListCreateAPIView: {str(e)}")
                return Response(
                    {"error": "Erro de integridade durante a criação em massa."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except Exception as e:
                logger.error(f"Erro durante criação em massa no CodigoListCreateAPIView: {str(e)}")
                return Response(
                    {"error": "Erro interno durante a criação em massa."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        # Se for objeto único, segue comportamento normal do DRF
        return super().post(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        Lida com requisições PUT para atualizar uma instância de CodigoEntrada.
        """
        try:
            return self.update(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Erro durante atualização no CodigoListCreateAPIView.put: {str(e)}")
            return Response(
                {"error": "Erro interno durante a atualização."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LocalDeChavesAPIView(generics.ListCreateAPIView):
    """
    API para listar e criar instâncias de CodigoEntrada filtradas por 'local_de_chaves'.
    """
    queryset = CodigoEntrada.objects.all()
    serializer_class = CodigoEntradaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['local_de_chaves']


class AdministracaoAPIView(generics.ListCreateAPIView):
    """
    API para listar e criar instâncias de CodigoEntrada filtradas por 'administracao'.
    """
    queryset = CodigoEntrada.objects.all()
    serializer_class = CodigoEntradaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['administracao']


class CodigoEntradaDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API para recuperar, atualizar ou deletar uma instância específica de CodigoEntrada.
    """
    queryset = CodigoEntrada.objects.all()
    serializer_class = CodigoEntradaSerializer

    def get(self, request, *args, **kwargs):
        """
        Recupera uma instância específica de CodigoEntrada.
        """
        try:
            return self.retrieve(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Erro ao recuperar CodigoEntradaDetailAPIView.get: {str(e)}")
            return Response(
                {"error": "Erro interno ao recuperar a instância."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, *args, **kwargs):
        """
        Atualiza uma instância específica de CodigoEntrada.
        """
        try:
            return self.update(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Erro ao atualizar CodigoEntradaDetailAPIView.put: {str(e)}")
            return Response(
                {"error": "Erro interno ao atualizar a instância."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, *args, **kwargs):
        """
        Deleta uma instância específica de CodigoEntrada.
        """
        try:
            return self.destroy(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Erro ao deletar CodigoEntradaDetailAPIView.delete: {str(e)}")
            return Response(
                {"error": "Erro interno ao deletar a instância."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class HomeView(generics.ListAPIView):
    """
    API para listar todas as instâncias de CodigoEntrada. Pode ser utilizada para exibir dados na página inicial.
    """
    queryset = CodigoEntrada.objects.all()
    serializer_class = CodigoEntradaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'localizacao',
        'instalacao',
        'codigos_da_porta',
        'codigo_caves',
        'local_de_chaves',
        'tipo_de_contrato',
        'administracao',
    ]

    def get(self, request, *args, **kwargs):
        """
        Lida com requisições GET para listar todas as instâncias de CodigoEntrada.
        """
        try:
            queryset = self.filter_queryset(self.get_queryset())

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Erro no HomeView.get: {str(e)}")
            return Response(
                {"error": "Erro interno no servidor."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
