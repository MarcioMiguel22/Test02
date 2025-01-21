from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from django.db import IntegrityError
from rest_framework.decorators import action

from .models import CodigoEntrada
from .serializers import CodigoEntradaSerializer


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
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to create a new CodigoEntrada instance.
        """
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
