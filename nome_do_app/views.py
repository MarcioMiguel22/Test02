from django.http import HttpResponse
from django.shortcuts import render
from .models import CodigoEntrada

# Create your views here.

def home(request):
    return render(request, 'nome_do_app/home.html')



from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import CodigoEntrada
from .serializers import CodigoEntradaSerializer

class CodigoEntradaViewSet(viewsets.ModelViewSet):
    queryset = CodigoEntrada.objects.all()
    serializer_class = CodigoEntradaSerializer

    def create(self, request, *args, **kwargs):
        # Handle bulk create
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['post'])
    def sync(self, request):
        # Clear existing data
        CodigoEntrada.objects.all().delete()
        
        # Create new entries
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
