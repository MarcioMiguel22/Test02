from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets, status, generics, permissions
from rest_framework.response import Response
from django.db import IntegrityError
from rest_framework.decorators import action, api_view
from rest_framework.views import APIView

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
    permission_classes = [permissions.AllowAny]  # Explicitly allow all users to access
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']  # Explicitly include DELETE

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

    def destroy(self, request, *args, **kwargs):
        """
        Implementação personalizada para operação DELETE.
        Remove um objeto CodigoEntrada específico e retorna status 204.
        """
        try:
            # Print debug info
            print(f"DELETE request received for ID: {kwargs.get('pk')}")

            # Get the object - this will raise 404 if not found
            instance = self.get_object()
            print(f"Object found: {instance}")
            
            # Attempt to delete
            self.perform_destroy(instance)
            
            # If we got here, deletion was successful
            print(f"Successfully deleted object with ID: {kwargs.get('pk')}")
            return Response(status=status.HTTP_204_NO_CONTENT)
            
        except CodigoEntrada.DoesNotExist:
            # Handle case where the object doesn't exist
            print(f"Object with ID {kwargs.get('pk')} not found")
            return Response(
                {"error": f"Registro com ID {kwargs.get('pk')} não encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            # Log the exception for debugging
            import traceback
            print(f"Error deleting object: {str(e)}")
            print(traceback.format_exc())
            
            return Response(
                {"error": f"Erro ao apagar registro: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )


# Add a debug view to test DELETE functionality
@api_view(['DELETE'])
def delete_debug(request, pk):
    """
    Debug endpoint to test DELETE functionality
    """
    try:
        instance = CodigoEntrada.objects.get(pk=pk)
        instance.delete()
        return Response({"status": "deleted"}, status=status.HTTP_200_OK)
    except CodigoEntrada.DoesNotExist:
        return Response({"error": "not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


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

    def put(self, request, *args, **kwargs):
        """
        Handle PUT requests to update a CodigoEntrada instance.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
