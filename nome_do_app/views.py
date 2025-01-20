from django.http import HttpResponse
from django.shortcuts import render

from rest_framework import viewsets, status
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

        # Caso recebamos uma lista de itens (bulk)
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
                    # Erros de validação
                    errors.append({
                        'item': item,
                        'error': serializer.errors
                    })

            # Retorna partial success (created + errors)
            return Response(
                {
                    'created': created_items,
                    'errors': errors,
                },
                status=status.HTTP_207_MULTI_STATUS  # 207 -> partial success
            )

        # Se for objeto único, usa a lógica padrão do DRF (criação "tudo ou nada")
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['post'])
    def sync(self, request):
        """
        Exemplo de ação customizada:
        - Deleta todos os registros
        - Cria novos registros de acordo com o POST recebido (lista).

        Aqui mantemos comportamento 'tudo ou nada':
        Se algum item falhar, dispara exceção e não cria nada.
        """
        CodigoEntrada.objects.all().delete()

        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
