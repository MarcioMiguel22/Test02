from django.shortcuts import render
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import DespesaCarro
from .serializers import DespesaCarroSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

class DespesaCarroViewSet(viewsets.ModelViewSet):
    serializer_class = DespesaCarroSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        queryset = DespesaCarro.objects.filter(usuario=user)
        
        # Filtrar por nome de utilizador se especificado
        username = self.request.query_params.get('username', None)
        if username and user.is_staff:  # Apenas administradores podem filtrar por outros utilizadores
            queryset = DespesaCarro.objects.filter(usuario__username=username)
            
        return queryset
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        search_term = request.query_params.get('search', '')
        username = request.query_params.get('username', None)
        
        queryset = self.get_queryset()
        
        if search_term:
            queryset = queryset.filter(
                Q(tipo_combustivel__icontains=search_term) |
                Q(valor_despesa__icontains=search_term) |
                Q(observacoes__icontains=search_term)
            )
            
        if username and request.user.is_staff:
            queryset = queryset.filter(usuario__username=username)
            
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user, usuario_criacao=self.request.user.username)
