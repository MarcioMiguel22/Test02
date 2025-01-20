# Importa a função HttpResponse do Django, que pode ser usada para retornar
# respostas HTTP simples como texto ou HTML.
from django.http import HttpResponse

# Importa a função render do Django, que simplifica o processo de renderizar
# templates HTML e retornar como resposta.
from django.shortcuts import render

# A view home é uma função simples que, quando chamada, renderiza um template
# chamado 'home.html'. Esse template deve estar localizado dentro de uma
# pasta de templates configurada no Django (por exemplo, 'templates/home.html').
def home(request):
    return render(request, 'home.html')


# Abaixo, temos importações específicas do Django Rest Framework (DRF)
# para criação de APIs.
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

# Importa o IntegrityError, útil caso um objeto viole constraints como unique=True
from django.db import IntegrityError

# Importa o modelo CodigoEntrada (que deve ser definido no arquivo models.py).
from .models import CodigoEntrada

# Importa o serializer CodigoEntradaSerializer (que também deve estar
# definido no arquivo serializers.py).
from .serializers import CodigoEntradaSerializer


class CodigoEntradaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para o modelo CodigoEntrada. Provê operações de CRUD.
    """

    queryset = CodigoEntrada.objects.all()
    serializer_class = CodigoEntradaSerializer

    def create(self, request, *args, **kwargs):
        """
        Lida com criação de registros.
        - Se receber uma lista, cria cada item individualmente (partial success).
        - Se receber um objeto único, faz o comportamento padrão.
        """
        data = request.data

        # Se for lista, faremos partial success
        if isinstance(data, list):
            created_items = []
            errors = []

            for item in data:
                # Cria um serializer para cada item individual
                serializer = self.get_serializer(data=item)

                # Verifica se o serializer é válido (campos obrigatórios, tipos, etc.)
                if serializer.is_valid():
                    try:
                        # Tenta salvar no banco
                        self.perform_create(serializer)
                        # Se criou com sucesso, adiciona à lista de criados
                        created_items.append(serializer.data)
                    except IntegrityError as e:
                        # Se houver um erro de integridade (ex.: unique=True duplicado),
                        # armazenamos para reportar ao cliente
                        errors.append({
                            'item': item,
                            'error': f"IntegrityError: {str(e)}"
                        })
                else:
                    # Se dados inválidos (falta campo, formato errado, etc.),
                    # guardamos as mensagens de erro
                    errors.append({
                        'item': item,
                        'error': serializer.errors
                    })

            # Retornamos 'partial success': alguns itens podem ter sido criados,
            # outros não. Aqui usamos 207 (Multi-Status), mas você pode usar 200.
            return Response(
                {
                    'created': created_items,
                    'errors': errors,
                },
                status=status.HTTP_207_MULTI_STATUS
            )

        # Se for um objeto único, chamar o método padrão (tudo ou nada).
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
