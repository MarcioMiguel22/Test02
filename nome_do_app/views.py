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

# Importa o modelo CodigoEntrada (que deve ser definido no arquivo models.py).
from .models import CodigoEntrada

# Importa o serializer CodigoEntradaSerializer (que também deve estar 
# definido no arquivo serializers.py).
from .serializers import CodigoEntradaSerializer


# Esta classe define um conjunto de views (ViewSet) para o modelo CodigoEntrada.
# Um ModelViewSet já provê as operações básicas de CRUD: listar, criar, 
# recuperar, atualizar e deletar registros.
class CodigoEntradaViewSet(viewsets.ModelViewSet):
    # Define o conjunto de dados (queryset) que será manipulado pelas operações.
    queryset = CodigoEntrada.objects.all()

    # Define qual serializer será utilizado para converter os objetos do 
    # banco de dados em JSON e vice-versa.
    serializer_class = CodigoEntradaSerializer

    # Sobrescrevemos o método create para adicionar a possibilidade de 
    # criação em lote (bulk create).
    def create(self, request, *args, **kwargs):
        # Verifica se os dados enviados são uma lista, o que indica 
        # que o usuário deseja criar vários registros de uma vez.
        if isinstance(request.data, list):
            # Cria uma instância do serializer com a opção many=True, 
            # pois é uma lista de objetos.
            serializer = self.get_serializer(data=request.data, many=True)

            # Valida os dados; se estiverem inválidos, gera um erro.
            serializer.is_valid(raise_exception=True)

            # Salva efetivamente os registros no banco de dados.
            self.perform_create(serializer)

            # Obtém os headers de sucesso (geralmente usado em conformidade 
            # com HTTP para inserir a localização do novo recurso).
            headers = self.get_success_headers(serializer.data)

            # Retorna a resposta com status 201 (Created) e os dados criados.
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        # Caso não seja uma lista, chamamos o método create padrão 
        # da classe pai (ModelViewSet) para criação de um registro único.
        return super().create(request, *args, **kwargs)

    # Aqui usamos o decorator @action para criar uma ação customizada na rota,
    # neste caso chamada 'sync'. Ela estará disponível no endpoint:
    # POST /codigoentrada/sync/ (sem precisar de um ID, pois detail=False).
    @action(detail=False, methods=['post'])
    def sync(self, request):
        # Primeiro, apagamos todos os registros existentes de CodigoEntrada
        # para depois inserir dados "sincronizados", conforme dados enviados.
        CodigoEntrada.objects.all().delete()

        # Novamente criamos instâncias do serializer em modo many=True, 
        # pois se espera receber vários registros.
        serializer = self.get_serializer(data=request.data, many=True)

        # Valida todos os registros recebidos.
        serializer.is_valid(raise_exception=True)

        # Salva os novos registros no banco de dados.
        self.perform_create(serializer)

        # Retorna a resposta com status 201 (Created) e os dados criados.
        return Response(serializer.data, status=status.HTTP_201_CREATED)
