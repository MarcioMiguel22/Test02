import logging
logger = logging.getLogger(__name__)

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from django.db import IntegrityError
from rest_framework.decorators import action
from rest_framework.views import APIView

from .models import CodigoEntrada
from .serializers import CodigoEntradaSerializer


def home(request):
    """
    Renderiza a página inicial (home.html).
    """
    return render(request, 'home.html')


class HomeView(APIView):
    def get(self, request):
        return Response({"message": "Welcome to the Home Page"}, status=status.HTTP_200_OK)


class CodigoEntradaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para o modelo CodigoEntrada. Provê operações de CRUD completas:
    list, retrieve, create, update, partial_update e destroy.
    """
    queryset = CodigoEntrada.objects.all()
    serializer_class = CodigoEntradaSerializer

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error in CodigoEntradaViewSet.list: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def create(self, request, *args, **kwargs):
        """
        Lida com criação de registros:
          - Se receber uma lista, cria cada item individualmente (partial success).
          - Se receber um objeto único, faz o comportamento normal.
        """

        data = request.data

        # Caso recebamos uma lista de itens
        if isinstance(data, list):
            created_items = []
            errors = []

            for item in data:
                serializer = self.get_serializer(data=item)
                if serializer.is_valid():
                    try:
                        self.perform_create(serializer)
                        created_items.append(serializer.data)
                    except IntegrityError as e:
                        # Se violar algum unique ou outra constraint do banco
                        errors.append({
                            'item': item,
                            'error': f"IntegrityError: {str(e)}"
                        })
                else:
                    errors.append({
                        'item': item,
                        'error': serializer.errors
                    })

            return Response(
                {
                    'created': created_items,
                    'errors': errors,
                },
                status=status.HTTP_207_MULTI_STATUS  # 207 indica partial success
            )

        # Se for objeto único, segue comportamento normal do DRF
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['post'])
    def sync(self, request):
        """
        Limpa todos os registros e insere novos. 
        Neste exemplo, mantém o comportamento 'tudo ou nada'.
        Se quiser partial success aqui também, basta usar lógica semelhante a 'create'.
        """
        CodigoEntrada.objects.all().delete()

        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CodigoListCreateAPIView(generics.ListCreateAPIView):
    queryset = CodigoEntrada.objects.all()
    serializer_class = CodigoEntradaSerializer

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests to list all CodigoEntrada instances.
        """
        queryset = self.get_queryset()

        # Filter by query parameters if provided
        localizacao = request.GET.get('localizacao')
        instalacao = request.GET.get('instalacao')
        codigos_da_porta = request.GET.get('codigos_da_porta')
        codigo_caves = request.GET.get('codigo_caves')
        local_de_chaves = request.GET.get('local_de_chaves')
        tipo_de_contrato = request.GET.get('tipo_de_contrato')
        administracao = request.GET.get('administracao')

        if localizacao:
            queryset = queryset.filter(localizacao=localizacao)
        if instalacao:
            queryset = queryset.filter(instalacao=instalacao)
        if codigos_da_porta:
            queryset = queryset.filter(codigos_da_porta=codigos_da_porta)
        if codigo_caves:
            queryset = queryset.filter(codigo_caves=codigo_caves)
        if local_de_chaves:
            queryset = queryset.filter(local_de_chaves=local_de_chaves)
        if tipo_de_contrato:
            queryset = queryset.filter(tipo_de_contrato=tipo_de_contrato)
        if administracao:
            queryset = queryset.filter(administracao=administracao)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to create a new CodigoEntrada instance.
        """
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        """
        Handle PUT requests to update a CodigoEntrada instance.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class LocalDeChavesAPIView(generics.ListAPIView):
    queryset = CodigoEntrada.objects.all()
    serializer_class = CodigoEntradaSerializer

class AdministracaoAPIView(generics.ListAPIView):
    queryset = CodigoEntrada.objects.all()
    serializer_class = CodigoEntradaSerializer

class CodigoEntradaDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CodigoEntrada.objects.all()
    serializer_class = CodigoEntradaSerializer
